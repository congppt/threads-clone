import os
from typing import Any
import uuid
from fastapi import HTTPException, status
from sqlalchemy import desc, exists, select
from db.models.user import User
from settings import Settings
from user.schemas import UserProfile, UserRegister
from sqlalchemy.ext.asyncio import AsyncSession
from user.utils import hash

AWS_BUCKET = os.getenv("AWS_BUCKET")


async def get_users_async(
    limit: int, before_id: int | None, username: str | None, db: AsyncSession
) -> dict[str, Any]:
    query = select(User).limit(limit + 1).order_by(desc(User.id))
    if before_id:
        query = query.where(User.id < before_id)
    if username:
        query = query.where(User.username.ilike(f"%{username}%"))
    result = await db.execute(query)
    users = result.scalars().all()
    has_more = len(users) > limit
    users = users[:limit]
    return {"users": users, "has_more": has_more}


async def create_user_async(request: UserRegister, db: AsyncSession):
    query = select(exists().where(User.username == request.username))
    if (await db.execute(query)).scalar():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exist!"
        )
    user = User(
        name=request.name,
        username=request.username,
        hashed_password=hash(request.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_id_async(id: int, db: AsyncSession):
    query = select(User).where(User.id == id)
    try:
        user = (await db.execute(query)).scalar_one()
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found",
        )


async def update_user_profile_async(request: UserProfile, user: User, db: AsyncSession):
    user.name = request.name
    user.image_url = request.image_url
    try:
        await db.commit()
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail=f"Profile not exist or accessible",
        )


def create_avatar_upload_url():
    s3 = Settings.get_aws_s3_client()
    object_name = "user-image/" + str(uuid.uuid4()) + ".jpeg"
    url = s3.generate_presigned_post(AWS_BUCKET, object_name, ExpiresIn=360)
    return url
