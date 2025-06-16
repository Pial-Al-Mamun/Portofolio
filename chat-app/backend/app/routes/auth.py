from fastapi import APIRouter

router = APIRouter()


@router.get("/authorize")
async def auth():
    return {"message": "Authentication endpoint is working!"}
