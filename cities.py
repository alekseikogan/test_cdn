from contextlib import asynccontextmanager

import geopy.distance
import requests
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.views import router as api_router
from db_helper import db_helper
from models import City


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(City.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan,
              title="Distance between cities")

app.include_router(api_router, prefix='/api/v1')


city_coordinates = {
    "Moscow": [55.7558, 37.6173],
    "Saint Petersburg": [59.9387, 30.3256],
    "Novosibirsk": [55.0415, 82.9343],
    "Yekaterinburg": [56.8519, 60.6122],
    "Nizhny Novgorod": [56.3269, 43.9962],
    "Rostov-on-Don": [47.2314, 39.7233],
    "Chelyabinsk": [55.1543, 61.4294],
    "Krasnoyarsk": [56.0184, 92.8672],
    "Saratov": [51.5333, 46.0333],
    "Vladivostok": [43.1242, 131.8867]
}


if __name__ == "__main__":
    uvicorn.run("cities:app", reload=True)
