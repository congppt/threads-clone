from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from db.database import get_db_async
from dependencies import get_current_user_async
from post.schemas import PostBase, PostDisplay
from post import service

post_router = APIRouter(prefix="/posts", tags=["Post"])

@post_router.get("/{id}", summary="Get post by id")
async def get_post_by_id_async(id: int = Path(ge=1), db = Depends(get_db_async)):
    return await service.get_post_by_id_async(id, db)

@post_router.get("", response_model= list[PostDisplay], summary="Get post list")
async def get_posts_async(user_id: Annotated[int | None, Query(None, ge=1)], before_id: Annotated[int | None, Query(None, ge=1)], limit : Annotated[int, Query(10, ge=1)], db = Depends(get_db_async)):
    return await service.get_posts_async(user_id, before_id, limit, db)

@post_router.post("", response_model=PostDisplay, summary="Create post")
async def create_post_async(request: PostBase, db = Depends(get_db_async), user = Depends(get_current_user_async)):
    return await service.create_post_async(request, user, db)

@post_router.put("/{id}", response_model=PostDisplay, summary="Update post")
async def update_post_async(request: PostBase, id: Annotated[int, Path(ge=1)], db = Depends(get_db_async), user = Depends(get_current_user_async)):
    return await service.update_post_async(id, request, user, db)

@post_router.delete("/{id}", summary="Delete post")
async def delete_post_async(id: int = Path(ge=1), db = Depends(get_db_async), user = Depends(get_current_user_async)):
    return await service.delete_post_async(id, user, db)

@post_router.get("/upload-image")
def get_presigned_url_async(user = Depends(get_current_user_async)):
    return service.create_presigned_url()