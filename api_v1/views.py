from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import db_helper

from . import crud
from .schemas import City, CityCreate

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


@router.get("/{city_id}", response_model=City)
async def get_product(city_id: int,
                      session: AsyncSession = Depends(db_helper.session_dependency),) -> City:
    """RETRIEVE - Получение города по id."""

    city = await crud.get_city(session=session, city_id=city_id)
    if city is not None:
        return city

    raise HTTPException(status_code=404, detail="City not found")


@router.post("", response_model=City)
async def create_product(
    city_in: CityCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """CREATE - Создание продукта."""

    return await crud.create_product(session=session, city_in=city_in)



# @router.delete("/{product_id}")
# async def delete_product(
#     product: City = Depends(product_by_id),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     """DELETE - Удаление продукта."""

#     await crud.delete_product(session=session, product=product)
#     return {
#         "success": True,
#         "message": f"Продукт id={product.id} {product.name} успешно удален!",
#     }


@router.get("/near")
async def read_near_cities(latitude: float, longitude: float):
    """Возвращает список двух ближайших городов."""

    pass
    # nearest_cities = []
    # for city in cities:
    #     distance = geopy.distance.geodesic((lat, lon), (city.coordinates[0], city.coordinates[1])).miles
    #     nearest_cities.append({"name": city.name, "distance": distance})
    # nearest_cities.sort(key=lambda x: x["distance"])
    # return nearest_cities[:2]
