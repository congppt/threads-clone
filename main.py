from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import message, post, user

load_dotenv()
app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins = origins, allow_headers = ["*"], allow_credentials=True, allow_methods=["*"])
app.include_router(user.router)
app.include_router(post.router)
app.include_router(message.router)