import os
from fastapi import APIRouter, Depends, Body, HTTPException, Path
from src.core.security import get_current_user
from src.llm.client import LLMClient
from src.llm.providers.openai import OpenAIProvider
from src.orgs.dependencies import org_access_dependency

router = APIRouter()

@router.post(
    "/{organization_id}/playground/prompt",
    dependencies=[Depends(org_access_dependency)],
)
def run_prompt(
    organization_id: str = Path(...),
    prompt: str = Body(..., embed=True),
    current_user: dict = Depends(get_current_user)
):
    """
    Runs a prompt in the playground.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable not set.")

    # In a real app, you would have a factory for providers and the client
    providers = [OpenAIProvider(api_key=openai_api_key)]
    llm_client = LLMClient(providers=providers)

    try:
        response = llm_client.generate(prompt=prompt, organization_id=organization_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
