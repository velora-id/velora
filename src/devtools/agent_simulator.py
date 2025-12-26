import os
from fastapi import APIRouter, Depends, Path, Body, HTTPException
from src.core.security import get_current_user
from src.orgs.dependencies import org_access_dependency
from src.core.firebase import get_db
from src.llm.client import LLMClient
from src.llm.providers.openai import OpenAIProvider

router = APIRouter()

@router.post(
    "/{organization_id}/agent-simulator/run",
    dependencies=[Depends(org_access_dependency)],
)
def run_agent_simulation(
    organization_id: str = Path(...),
    agent_id: str = Body(..., embed=True),
    input_data: dict = Body(..., embed=True),
    current_user: dict = Depends(get_current_user)
):
    """
    Runs a simulation of an agent.
    """
    db = get_db()
    agent_ref = db.collection("organizations").document(organization_id).collection("agents").document(agent_id)
    agent_doc = agent_ref.get()

    if not agent_doc.exists:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent_data = agent_doc.to_dict()
    system_prompt = agent_data.get("system_prompt", "You are a helpful assistant.")

    # A simple way to include input_data in the prompt.
    # In a real application, you might use a more sophisticated templating engine.
    prompt = system_prompt
    if input_data and 'text' in input_data:
        prompt += f"\n\nUser: {input_data['text']}\nAssistant:"


    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable not set.")

    providers = [OpenAIProvider(api_key=openai_api_key)]
    llm_client = LLMClient(providers=providers)

    try:
        response = llm_client.generate(prompt=prompt, organization_id=organization_id)
        return {"simulation_output": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
