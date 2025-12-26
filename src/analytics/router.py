from fastapi import APIRouter, Depends

from src.core.firebase import get_db
from .service import get_analytics_overview

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("/{organization_id}")
async def http_get_analytics_overview(organization_id: str, db=Depends(get_db)):
    """Gets an overview of analytics for an organization."""
    return get_analytics_overview(db, organization_id)
