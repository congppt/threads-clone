from contextlib import asynccontextmanager
import logging
import logging.config
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from routers import routers
from redis.asyncio import Redis
from db.database import redis_pool
from settings import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

load_dotenv()

origins = os.getenv("ALLOWED_ORGS").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App started")
    redis = Redis(connection_pool=redis_pool)
    await FastAPILimiter.init(redis)
    yield
    logger.info("App shutdown")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

for router in routers:
    app.include_router(router)
