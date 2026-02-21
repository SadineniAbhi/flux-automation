from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from models.database import init_db
from routes.default import router as default_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(default_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)