from fastapi import APIRouter


router = APIRouter()


@router.app("/auth")
async def auth():
    return {"message": "Authentication endpoint is working!"}


@router.post("")
async def login():
    pass


@router.post("")
async def register():
    pass
