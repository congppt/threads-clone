from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import delete, desc, select, update
from models.post import Post
from dtos.post import PostBase
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import engine

async def create_post_async(request: PostBase, user: int, db: AsyncSession):
    post = Post(user_id = user, content = request.content, image_url = request.image_url, created_at = datetime.now(timezone.utc))
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def get_post_by_id_async(id: int, db: AsyncSession):
    query = select(Post).where(Post.id == id, Post.is_deleted == False)
    try:
        user = (await db.execute(query)).scalar_one()
        return user
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

async def get_posts_async(user_id: Optional[int], before_id: Optional[int], limit: int, db : AsyncSession):
    query = select(Post).order_by(desc(Post.id)).limit(limit)
    if before_id is not None:
        query = query.where(Post.id < before_id)
    if user_id is not None:
        query = query.where(Post.user_id == user_id)
    posts = (await db.execute(query)).scalars().all()
    return posts

async def delete_post_async(id: int, db : AsyncSession):
    command = update(Post).where(Post.id == id, Post.is_deleted == False).values(is_deleted=1)
    print(command.compile(engine, compile_kwargs={"literal_binds": True}))
    result = await db.execute(command)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return "Deleted"