from typing import List

import requests
from fastapi import HTTPException
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import City

from .schemas import CityCreate

API_KEY = 'd25fe013c17545d48a5d4a6659c0d1ff'


def get_coordinates_of_city(name):
    """GET - Получение координат города по названию через внешний API."""
    response = requests.get(
        f"https://api.geoapify.com/v1/geocode/search?text={name}&limit=1&type=city&apiKey={API_KEY}"
    )
    if response.status_code == 200:
        data = response.json().get('features')[0]['properties']
        latitude = data.get("lat")
        longitude = data.get("lon")
        return {
            "name": name,
            'latitude': latitude,
            'longitude': longitude
        }
    else:
        raise HTTPException(status_code=404, detail="City in API server not found!")


async def get_cities(session: AsyncSession) -> List[City]:
    """GET - Получение всех городов."""

    stmt = select(City).order_by(City.id).limit(5)
    result: Result = await session.execute(stmt)
    cities = result.scalars().all()
    return list(cities)


async def get_city(session: AsyncSession, name: str) -> City | None:
    """RETRIEVE - Получение города по названию."""

    query = select(City).where(City.name == name)
    result = await session.execute(query)
    city = result.scalars().first()
    return city


async def create_city(session: AsyncSession, name: str) -> dict:
    """CREATE - Создание города."""

    city_in = get_coordinates_of_city(name)  # загрузка геопозиции с API
    if city_in is not None:
        city = City(**city_in)
        session.add(city)
        await session.commit()
        return city


# async def delete_city(session: AsyncSession, city: City) -> City:
#     """DELETE - Удаление продукта."""

#     await session.delete(сity)
#     await session.commit()
