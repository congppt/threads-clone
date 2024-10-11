from typing import Optional
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

class UserProfile(BaseModel):
    name: str
    image_url: str | None