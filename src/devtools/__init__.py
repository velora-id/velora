from fastapi import APIRouter
from .prompt_playground import router as prompt_playground_router
from .agent_simulator import router as agent_simulator_router
from .workflow_tester import router as workflow_tester_router
from .api_explorer import router as api_explorer_router

router = APIRouter()

router.include_router(prompt_playground_router, tags=["devtools"])
router.include_router(agent_simulator_router, tags=["devtools"])
router.include_router(workflow_tester_router, tags=["devtools"])
router.include_router(api_explorer_router, tags=["devtools"])
