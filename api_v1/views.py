from typing import List

import geopy.distance
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import db_helper

from . import crud
from .schemas import City

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.get("", response_model=List[City])
async def get_cities(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """GET - Получение всех городов."""

    return await crud.get_cities(session=session)


@router.get("/{name}", response_model=City)
async def get_city_by_name(
    name: str,
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> City:
    """RETRIEVE - Получение города по названию."""

    city = await crud.get_city(session=session, name=name)
    if city is not None:
        return city

    raise HTTPException(status_code=404, detail="City not found")


@router.post("", response_model=City)
async def create_city(
    name: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> City:
    """CREATE - Создание записи города в базу данных."""

    return await crud.create_city(session=session, name=name)


@router.delete("/{name}")
async def delete_city(
    name: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """DELETE - Удаление города по названию."""

    city = await crud.get_city(session=session, name=name)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Города {name} нет в базе!',
        )

    await crud.delete_city(session=session, city=city)
    return {
        "success": True,
        "message": f"Город {city.name} успешно удален!",
    }


@router.post("/near")
async def read_near_cities(
    latitude: float,
    longitude: float,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    """Возвращает список двух ближайших городов."""

    nearest_cities = []
    cities = await crud.get_cities(session=session)

    for city in cities:
        distance = geopy.distance.geodesic(
            (latitude, longitude), (city.latitude, city.longitude)).kilometers
        nearest_cities.append({"name": city.name, "distance_km": distance})
    nearest_cities.sort(key=lambda x: x["distance_km"])
    return nearest_cities[1:3]
