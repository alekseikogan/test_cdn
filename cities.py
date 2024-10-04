from contextlib import asynccontextmanager
import geopy.distance
import requests
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import db_helper
from models import City
from schemas import CityCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(City.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan,
              title="Distance between cities")

API_KEY = 'd25fe013c17545d48a5d4a6659c0d1ff'


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


@app.post("/cities/")
async def create_city(
    # city_name: str,
    # city_in: CityCreate,
    # session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Получает координаты города с внешнего API и добавляет его в базу данных."""

    pass
    # response = requests.get(
    #     f"https://api.geoapify.com/v1/geocode/search?text={city_name}&limit=1&type=city&apiKey={API_KEY}"
    # )

    # if response.status_code == 200:
    #     data = response.json().get('features')[0].get('properties')
    #     lat = data.get("lat")
    #     lon = data.get("lon")
    #     city = City(**city_in.model_dump())
    #     session.add(city)
    #     await session.commit()
    #     return {
    #         'city': city,
    #         "message": "Город успешно добавлен в базу данных"}
    # else:
    #     raise HTTPException(status_code=404, detail="City not found")


@app.get("/cities/")
async def read_cities():
    """Возвращает список городов."""

    pass


@app.get("/cities/near/")
async def read_near_cities(lat: float, lon: float):
    """Возвращает список двух ближайших городов."""

    pass
    # nearest_cities = []
    # for city in cities:
    #     distance = geopy.distance.geodesic((lat, lon), (city.coordinates[0], city.coordinates[1])).miles
    #     nearest_cities.append({"name": city.name, "distance": distance})
    # nearest_cities.sort(key=lambda x: x["distance"])
    # return nearest_cities[:2]


@app.delete("/cities/delete/")
def delete_city():
    """Удаляет город из базы данных."""

    pass
    # if city.name in city_coordinates:
    #     del city_coordinates[city_name]
    #     print(f"City '{city_name}' has been deleted from the database.")
    # else:
    #     print(f"City '{city_name}' not found in the database.")
    # return city_coordinates


if __name__ == "__main__":
    uvicorn.run("cities:app", reload=True)
