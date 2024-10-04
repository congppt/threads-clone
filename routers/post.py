from fastapi import APIRouter, Depends

from db.database import get_db_async
from schemas import PostBase, PostDisplay
from services.user import get_current_user_async
from services import post as service

router = APIRouter(prefix="/posts", tags=["post"], dependencies=[Depends(get_current_user_async)])

@router.get("")
async def get_posts():
    return "Posts"

@router.post("", response_model=PostDisplay)
async def create_post(request: PostBase, db = Depends(get_db_async), user= Depends(get_current_user_async)):
    post = await service.create_post_async(request, user, db)
    return post