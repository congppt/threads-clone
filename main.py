import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins = origins, allow_headers = ["*"], allow_credentials=True, allow_methods=["*"])