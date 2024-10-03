from datetime import datetime, timezone
from models.post import Post
from schemas import PostBase
from sqlalchemy.ext.asyncio import AsyncSession

async def create_post_async(request: PostBase, user: int, db: AsyncSession):
    post = Post(user_id = user, content = request.content, image_url = request.image_url, created_at = datetime.now(timezone.utc))
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post