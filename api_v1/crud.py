from typing import List

import requests
from fastapi import HTTPException
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import City

from .schemas import CityCreate

API_KEY = 'd25fe013c17545d48a5d4a6659c0d1ff'


def get_coordinates_of_city(name):
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

    stmt = select(City).order_by(City.id)
    result: Result = await session.execute(stmt)
    cities = result.scalars().all()
    return list(cities)


async def get_city(session: AsyncSession, city_id: int) -> City | None:
    """RETRIEVE - Получение города по id."""

    return await session.get(City, city_id)


async def create_city(session: AsyncSession, name: str) -> dict:
    """CREATE - Создание города."""

    # ТУТ добавить логику работы с API
    city_in = get_coordinates_of_city(name)
    if city_in is not None:
        city = City(**city_in)
        session.add(city)
        await session.commit()
        return city


# async def delete_city(session: AsyncSession, product: City) -> City:
#     """DELETE - Удаление продукта."""

#     await session.delete(product)
#     await session.commit()
