from fastapi import Request
from .service import log_activity
from src.core.firebase import get_db

async def audit_log_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # This is a basic implementation. You may want to expand this to capture more details.
    if "organization_id" in request.path_params and "user" in request.state:
        log_activity(
            db=get_db(),
            organization_id=request.path_params["organization_id"],
            user_id=request.state.user["uid"],
            action=f"{request.method} {request.url.path}",
            details={
                "status_code": response.status_code,
                "path_params": request.path_params,
            }
        )

    return response
