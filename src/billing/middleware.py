from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import RequestResponseFunction
from starlette.responses import Response
from src.core.firebase import get_db
import re
import datetime

class QuotaEnforcementMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseFunction) -> Response:
        # This middleware should not apply to auth or billing routes
        if any(request.url.path.startswith(prefix) for prefix in ["/auth", "/billing", "/docs", "/openapi.json"]):
            return await call_next(request)

        org_id_match = re.search(r"/orgs/(\\w+)", request.url.path)
        if not org_id_match:
            # If the path does not contain an organization ID, let it pass.
            # This could be for general, non-org-specific routes.
            return await call_next(request)
        
        organization_id = org_id_match.group(1)
        db = get_db()
        now = datetime.datetime.utcnow()
        month_str = now.strftime("%Y-%m")

        subscriptions_ref = db.collection(f'organizations/{organization_id}/subscriptions').where("status", "==", "active").limit(1)
        active_subscriptions = list(subscriptions_ref.stream())

        if not active_subscriptions:
            raise HTTPException(status_code=403, detail="No active subscription found for this organization.")
        
        subscription = active_subscriptions[0].to_dict()
        quota = subscription.get("quotas", {}).get("requests", 0)

        usage_ref = db.collection(f'organizations/{organization_id}/usage').document(month_str)
        usage_doc = usage_ref.get()

        if not usage_doc.exists:
            usage_ref.set({"requests": 0})
            current_usage = 0
        else:
            current_usage = usage_doc.to_dict().get("requests", 0)

        if current_usage >= quota:
            raise HTTPException(status_code=429, detail="Monthly request quota exceeded.")
        
        usage_ref.update({"requests": current_usage + 1})

        response = await call_next(request)
        return response
