from typing import Optional
from fastapi import APIRouter, Depends, Path, Query

from db.database import get_db_async
from dtos.post import PostBase, PostDisplay
from services.user import get_current_user_async
from services import post as service

router = APIRouter(prefix="/posts", tags=["post"])

@router.get("/{id}")
async def get_post_by_id_async(id: int = Path(ge=1), db = Depends(get_db_async)):
    return await service.get_post_by_id_async(id, db)

@router.get("", response_model= list[PostDisplay])
async def get_posts_async(user_id: Optional[int] = Query(None, ge=1), before_id: Optional[int] = Query(None, ge=1), limit : int = Query(10, ge=1),db = Depends(get_db_async)):
    return await service.get_posts_async(user_id, before_id, limit, db)

@router.post("", response_model=PostDisplay)
async def create_post_async(request: PostBase, db = Depends(get_db_async), user = Depends(get_current_user_async)):
    return await service.create_post_async(request, user, db)

@router.put("/{id}", response_model=PostDisplay)
async def update_post_async(request: PostBase, id: int = Path(ge=1), db = Depends(get_db_async), user = Depends(get_current_user_async)):
    return await service.update_post_async(id, request, user, db)

@router.delete("/{id}")
async def delete_post_async(id: int = Path(ge=1), db = Depends(get_db_async), user = Depends(get_current_user_async)):
    return await service.delete_post_async(id, user, db)

