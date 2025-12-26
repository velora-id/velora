from fastapi import APIRouter
from fastapi.routing import APIRoute
from src.app import app

router = APIRouter()

@router.get("/api-explorer/endpoints")
def get_api_endpoints():
    """
    Returns a detailed list of all available API endpoints, including methods and descriptions.
    """
    endpoint_list = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            # Extracting docstring for description
            docstring = route.endpoint.__doc__
            description = docstring.strip() if docstring else "No description available."

            endpoint_list.append({
                "path": route.path,
                "name": route.name,
                "methods": sorted(list(route.methods)),
                "description": description
            })

    return sorted(endpoint_list, key=lambda x: x['path'])
