import os
from typing import Any,  Optional
import uuid
from fastapi import HTTPException, status
from sqlalchemy import desc, select
from db.models.post import Post
from post.schemas import PostBase
from sqlalchemy.ext.asyncio import AsyncSession
from settings import Settings

AWS_BUCKET = os.getenv("AWS_BUCKET")

async def create_post_async(request: PostBase, user: dict[str, Any], db: AsyncSession):
    post = Post(user_id = int(user["id"]), content = request.content, image_url = request.image_url)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def get_post_by_id_async(id: int, db: AsyncSession):
    query = select(Post).where(Post.id == id, Post.is_deleted == False)
    try:
        post = (await db.execute(query)).scalar_one()
        return post
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

async def delete_post_async(id: int, user: dict[str, Any], db : AsyncSession):
    post = await get_post_by_id_async(id, db)
    if post.user_id != int(user["id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    post.is_deleted = True
    try:
        await db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=f"Post not exist or accessible")
    # command = update(Post).where(Post.id == id, Post.is_deleted == False).values(is_deleted=True)
    # result = await db.execute(command)
    # await db.commit()
    # if result.rowcount == 0:
    #     raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=f"Post not exist or accessible")
    return "Deleted"

async def update_post_async(id: int, request: PostBase, user: dict[str, Any], db: AsyncSession):
    post = await get_post_by_id_async(id, db)
    if post.user_id != int(user["id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    post.content = request.content
    post.image_url = request.image_url
    try:
        await db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=f"Post not exist or accessible")
    # command = update(Post).where(Post.id == id, Post.is_deleted == False).values(content = request.content, image_url = request.image_url)
    # result = await db.execute(command)
    # await db.commit()
    # if result.rowcount == 0:
    #     raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=f"Post no longer exist or accessible")
    return post

def create_presigned_url():
    s3 = Settings.get_aws_s3_client()
    object_name = str(uuid.uuid4())
    url = s3.generate_presigned_post(AWS_BUCKET, object_name, ExpiredIn=360)
    return url