from fastapi import APIRouter

router = APIRouter()


@router.get("/models")
def get_models():
    return {
        "data": [
            {"id": "gpt-3.5-turbo", "object": "model", "owned_by": "owner"},
            {"id": "gpt-4", "object": "model", "owned_by": "owner"},
        ],
        "object": "list",
    }
