from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    username: str
    password: str
    year_of_birth: int


class UserDisplay(BaseModel):
    username: str
    name: str
    image_url: str
    

class GameBase(BaseModel):
    name: str
    img_url: str

