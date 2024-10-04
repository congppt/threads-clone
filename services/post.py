from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy import delete, select
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
    query = select(Post).where(Post.id == id and not Post.is_deleted)
    try:
        user = (await db.execute(query)).scalar_one()
        return user
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    
async def delete_post_async(id: int, db : AsyncSession):
    command = delete(Post).where(Post.id == id)
    result = await db.execute(command)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return "Deleted"