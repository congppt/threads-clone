from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    image_url: str | None
    content: str | None

class PostDisplay(PostBase):
    id: int
    created_at: datetime
    user_id: int
    model_config=ConfigDict(from_attributes=True)