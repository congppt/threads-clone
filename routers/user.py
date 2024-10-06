from fastapi import APIRouter, Depends, Path, Query
from fastapi.security import OAuth2PasswordRequestForm
from services import user as service
from db.database import get_db_async
from dtos.user import UserDisplay, UserRegister

router = APIRouter(prefix="/users", tags=["user"])

@router.get("")
async def get_users_async(username: str = Query(), pageSize : int = Query(ge=1), db = Depends(get_db_async)):
    return "users"

@router.get("/{id}", response_model=UserDisplay)
async def get_user_by_id_async(id: int = Path(ge=1), db = Depends(get_db_async)):
    return await service.get_user_by_id_async(id, db)
@router.post("", response_model=UserDisplay)
async def create_user_async(request: UserRegister, db = Depends(get_db_async)):
    return await service.create_user_async(request, db)

@router.post("/auth")
async def auth_async(request: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db_async)):
    return await service.auth_async(request, db)