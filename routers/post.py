from fastapi import APIRouter, Depends, Path

from db.database import get_db_async
from dtos.post import PostBase, PostDisplay
from services.user import get_current_user_async
from services import post as service

router = APIRouter(prefix="/posts", tags=["post"], dependencies=[Depends(get_current_user_async)])

@router.get("")
async def get_posts_async():
    return "Posts"

@router.get("/{id}")
async def get_post_by_id_async(id: int = Path(ge=1), db = Depends(get_db_async)):
    return await service.get_post_by_id_async(id, db)

@router.post("", response_model=PostDisplay)
async def create_post_async(request: PostBase, db = Depends(get_db_async), user= Depends(get_current_user_async)):
    return await service.create_post_async(request, user, db)

@router.delete("/{id}")
async def delete_post_async(id: int = Path(ge=1), db = Depends(get_db_async)):
    return await service.delete_post_async(id, db)

