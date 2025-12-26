import os
from fastapi import APIRouter, Depends, Path, Body, HTTPException
from src.core.security import get_current_user
from src.orgs.dependencies import org_access_dependency
from src.core.firebase import get_db
from src.llm.client import LLMClient
from src.llm.providers.openai import OpenAIProvider

router = APIRouter()

# This is a simplified execution engine for the tester.
# A real engine would be more robust, handle errors, state, etc.
def execute_step(step, current_context, llm_client, organization_id):
    step_type = step.get("type")
    step_id = step.get("id")
    step_output = None
    status = "success"

    try:
        if step_type == "llm":
            # Use the LLM client, similar to the agent simulator
            prompt_template = step.get("prompt", "No prompt in step.")
            # Simple templating: replace placeholders like {{input.text}}
            prompt = prompt_template.replace("{{input.text}}", current_context.get("text", ""))

            response = llm_client.generate(prompt=prompt, organization_id=organization_id)
            step_output = {"response": response}

        elif step_type == "api":
            # Simulate calling an external API
            url = step.get("url", "no-url-provided")
            method = step.get("method", "GET")
            step_output = {"status": "success", "message": f"Simulated {method} call to {url}"}

        elif step_type == "condition":
            # Simulate a conditional branch
            # This is a very basic simulation. A real one would evaluate expressions.
            step_output = {"condition_met": True, "message": "Condition evaluated to true"}

        else:
            status = "skipped"
            step_output = {"message": f"Step type '{step_type}' is not supported by the tester yet."}

    except Exception as e:
        status = "failed"
        step_output = {"error": str(e)}

    return {
        "step_id": step_id,
        "type": step_type,
        "status": status,
        "output": step_output
    }


@router.post(
    "/{organization_id}/workflow-tester/run",
    dependencies=[Depends(org_access_dependency)],
)
def run_workflow_test(
    organization_id: str = Path(...),
    workflow_id: str = Body(..., embed=True),
    input_data: dict = Body(..., embed=True),
    current_user: dict = Depends(get_current_user)
):
    """
    Tests a workflow by simulating the execution of its steps.
    """
    db = get_db()
    workflow_ref = db.collection("organizations").document(organization_id).collection("workflows").document(workflow_id)
    workflow_doc = workflow_ref.get()

    if not workflow_doc.exists:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow_data = workflow_doc.to_dict()
    steps = workflow_data.get("steps", [])

    if not steps:
        return {"workflow_id": workflow_id, "status": "success", "log": [], "final_output": input_data, "message": "Workflow has no steps to execute."}

    # Setup LLM Client for steps that need it
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable not set.")
    providers = [OpenAIProvider(api_key=openai_api_key)]
    llm_client = LLMClient(providers=providers)

    execution_log = []
    current_context = input_data

    for step in steps:
        step_result = execute_step(step, current_context, llm_client, organization_id)
        execution_log.append(step_result)

        if step_result["status"] == "success":
            # Update context for the next step.
            # This is a simple merge; a real engine might have more complex state management.
            if step_result["output"]:
                current_context.update(step_result["output"])
        else:
            # Stop execution on failure
            return {"workflow_id": workflow_id, "status": "failed", "log": execution_log, "final_output": current_context}


    return {"workflow_id": workflow_id, "status": "success", "log": execution_log, "final_output": current_context}
