from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.default import router as default_router
from routes.project import router as project_router
from utils.db import create_db_and_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(default_router)
app.include_router(project_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)