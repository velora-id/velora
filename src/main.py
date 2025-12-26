import os
import uvicorn
from fastapi import Depends, Request, HTTPException

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from config.settings import settings
from src.core.firebase import initialize_firebase, get_db
from src.core.security import get_current_user
from src.auth.routes import router as auth_router
from src.orgs.routes import router as org_router
from src.agents.routes import router as agents_router
from src.workflows.routes import router as workflows_router
from src.tasks.routes import router as tasks_router
from src.analytics.router import router as analytics_router
from src.audit.router import router as audit_router
from src.billing.router import router as billing_router
from src.credits.router import router as credits_router
from src.devtools import router as devtools_router
from src.core.ratelimit import limiter
from src.core.roles import Role, require_role
from src.core.logging import logging_middleware
from src.audit.middleware import audit_log_middleware
from src.billing.middleware import QuotaEnforcementMiddleware
from src.app import app

initialize_firebase()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)
app.middleware("http")(logging_middleware)
app.middleware("http")(audit_log_middleware)
app.add_middleware(QuotaEnforcementMiddleware)


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(org_router, prefix="/orgs", tags=["orgs"])
app.include_router(agents_router, prefix="/orgs", tags=["agents"])
app.include_router(workflows_router, prefix="/orgs", tags=["workflows"])
app.include_router(tasks_router, prefix="/orgs", tags=["tasks"])
app.include_router(analytics_router, prefix="/orgs", tags=["analytics"])
app.include_router(audit_router, prefix="/orgs", tags=["audit"])
app.include_router(billing_router, prefix="/billing", tags=["billing"])
app.include_router(credits_router, prefix="/orgs", tags=["credits"])
app.include_router(devtools_router, prefix="/orgs", tags=["devtools"])


@app.get("/")
@limiter.limit("10/minute")
def read_root(request: Request):
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return {"message": f"Hello {name}!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/ready")
def readiness_check():
    try:
        db = get_db()
        # A simple check to confirm Firestore access.
        # This will attempt to get a document that may not exist,
        # but the operation itself is a valid check of connectivity.
        db.collection(u'__health_check').document(u'readiness').get()
        return {"status": "ok", "message": "Service is ready and connected to Firebase."}
    except Exception as e:
        # The service is not ready if it cannot connect to the database.
        raise HTTPException(status_code=503, detail=f"Service Unavailable: Could not connect to Firebase. Reason: {e}")

@app.get("/example")
def example_firestore():
    db = get_db()
    doc_ref = db.collection(u'test').document(u'example')
    doc_ref.set({
        u'foo': u'bar'
    })
    return {"status": "ok"}

@app.get("/test-auth", dependencies=[Depends(require_role(Role.ADMIN))])
async def test_auth(current_user: dict = Depends(get_current_user)):
    return {"message": "Authenticated and you are an admin!", "user": current_user}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", settings.PORT))
    uvicorn.run("main:app", host=settings.HOST, port=port, reload=settings.RELOAD)
