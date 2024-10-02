from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import message as Message, post as Post, user as User

load_dotenv()
app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins = origins, allow_headers = ["*"], allow_credentials=True, allow_methods=["*"])
app.include_router(User.router)
app.include_router(Post.router)
app.include_router(Message.router)