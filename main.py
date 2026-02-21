from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.default import router as default_router
from utils.db import create_db_and_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(default_router)