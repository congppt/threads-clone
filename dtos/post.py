from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    image_url: Optional[str]
    content: Optional[str]

class PostDisplay(PostBase):
    id: int
    created_at: datetime
    user_id: int
    model_config=ConfigDict(from_attributes=True)