from fastapi import APIRouter, Depends
from services import user as service
from db.database import get_db_async
from schemas import UserBase, UserDisplay, UserRegister

router = APIRouter(prefix="/users", tags=["user"])

@router.get("")
async def get_users():
    return "users"

@router.post("", response_model=UserDisplay)
async def create_user(request: UserRegister, db = Depends(get_db_async)):
    return await service.create_user(request, db)