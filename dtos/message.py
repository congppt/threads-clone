from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    content: str
    to_user_id: int

class MessageDisplay(MessageBase):
    id: int
    created_at: datetime
    from_user_id: int
    model_config=ConfigDict(from_attributes=True)