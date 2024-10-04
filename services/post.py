from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy import select
from models.post import Post
from schemas import PostBase
from sqlalchemy.ext.asyncio import AsyncSession

async def create_post_async(request: PostBase, user: int, db: AsyncSession):
    post = Post(user_id = user, content = request.content, image_url = request.image_url, created_at = datetime.now(timezone.utc))
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def get_post_by_id_async(id: int, db: AsyncSession):
    query = select(Post).where(Post.id == id)
    try:
        user = (await db.execute(query)).scalar_one()
        return user
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")