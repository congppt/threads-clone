from fastapi import APIRouter, Depends, Path, Query
from db.database import get_db_async
from dependencies import get_current_user_async
from user import service
from user.schemas import UserDisplay, UserProfile, UserRegister


user_router = APIRouter(prefix="/users", tags=["User"])

@user_router.get("", summary="Get user list")
async def get_users_async(username: str = Query(), pageSize : int = Query(ge=1), db = Depends(get_db_async)):
    return "users"

@user_router.get("/{id}", response_model=UserDisplay, summary="Get user by id")
async def get_user_by_id_async(id: int = Path(ge=1), db = Depends(get_db_async)):
    return await service.get_user_by_id_async(id, db)

@user_router.post("", response_model=UserDisplay, summary="Register user")
async def create_user_async(request: UserRegister, db = Depends(get_db_async)):
    return await service.create_user_async(request, db)

@user_router.put("", response_model=UserDisplay, summary="Update user profile")
async def update_user_profile_async(request: UserProfile, user = Depends(get_current_user_async), db = Depends(get_db_async)):
    return await service.update_user_profile_async(request, user, db)