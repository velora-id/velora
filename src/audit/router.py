from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
import io
import csv
from src.core.firebase import get_db
from src.core.roles import require_org_role, OrgRole
from typing import Optional, List
from .models import AuditLogInDB

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
)

@router.get(
    "/{organization_id}/logs",
    response_model=List[AuditLogInDB],
    dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN]))]
)
def get_audit_logs(
    organization_id: str,
    user_id: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db = Depends(get_db)
):
    """Get audit logs for an organization with optional filtering and pagination."""
    query = db.collection(f'organizations/{organization_id}/audit_logs')

    if user_id:
        query = query.where('user_id', '==', user_id)
    if action:
        query = query.where('action', '==', action)

    logs = [AuditLogInDB(**doc.to_dict()) for doc in query.limit(limit).offset(offset).stream()]
    return logs

@router.get(
    "/{organization_id}/logs/export",
    dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN]))]
)
def export_audit_logs_to_csv(
    organization_id: str,
    user_id: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    db = Depends(get_db)
):
    """Export audit logs to a CSV file."""
    query = db.collection(f'organizations/{organization_id}/audit_logs')

    if user_id:
        query = query.where('user_id', '==', user_id)
    if action:
        query = query.where('action', '==', action)

    logs_stream = query.stream()

    def generate_csv():
        output = io.StringIO()
        writer = None

        for doc in logs_stream:
            log_data = doc.to_dict()
            if writer is None:
                writer = csv.DictWriter(output, fieldnames=log_data.keys())
                writer.writeheader()
            
            writer.writerow(log_data)
            output.seek(0)
            yield output.read()
            output.seek(0)
            output.truncate(0)

    response = StreamingResponse(generate_csv(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=audit_logs.csv"
    return response
