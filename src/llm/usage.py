from src.core.firebase import get_db
from src.llm.models import LLMUsage

def record_usage(db, organization_id: str, usage_data: LLMUsage):
    """Records LLM usage data in Firestore."""
    db.collection('organizations').document(organization_id).collection('llm_usages').add(usage_data.dict())
