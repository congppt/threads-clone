from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import routers

logger = logging.getLogger(__name__)

load_dotenv()

origins = os.getenv("ALLOWED_ORGS").split(",")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App started")
    yield
    logger.info("App shutdown")

app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins = origins, allow_headers = ["*"], allow_credentials=True, allow_methods=["*"])

for router in routers:
    app.include_router(router)

