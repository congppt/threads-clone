from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    username: str

class UserRegister(UserBase):
    password: str
class UserDisplay(UserBase):
    id: int
    image_url: str | None
    model_config=ConfigDict(from_attributes=True)
    

class PostBase(BaseModel):
    img_url: str | None
    content: str | None

class PostDisplay(PostBase):
    id: int
    created_at: datetime
    user: UserBase
    model_config=ConfigDict(from_attributes=True)

class MessageBase(BaseModel):
    content: str
    to_user_id: int

class MessageDisplay(MessageBase):
    id: int
    created_at: datetime
    from_user_id: int
    model_config=ConfigDict(from_attributes=True)

