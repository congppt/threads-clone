from fastapi import APIRouter

router = APIRouter(prefix="/posts", tags=["post"])

@router.get("")
async def get_posts():
    return "Posts"