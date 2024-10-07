from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1.views import router as api_router
from db_helper import db_helper
from models import City


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(City.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan,
              title="Distance between cities")

app.include_router(api_router, prefix='/api/v1')


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
