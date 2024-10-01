from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    username: str

class UserRegister(UserBase):
    password: str
class UserDisplay(UserBase):
    id: int
    image_url: str | None
    

class PostBase(BaseModel):
    img_url: str | None
    content: str | None

class PostDisplay(PostBase):
    id: int
    created_at: datetime
    user: UserBase

class MessageBase(BaseModel):
    content: str

class MessageDisplay(MessageBase):
    id: int
    created_at: datetime
