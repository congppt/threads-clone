from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["user"])

@router.get("")
async def get_users():
    return "users"