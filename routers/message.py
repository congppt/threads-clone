from fastapi import APIRouter

router = APIRouter(prefix="/messages", tags=["message"])

@router.get("")
async def get_messages():
    return "messages"