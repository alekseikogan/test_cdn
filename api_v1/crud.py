from typing import List

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import TownCreate, TownPartialUpdate, TownUpdate
from core.models import Town


async def get_products(session: AsyncSession) -> List[Town]:
    """GET - Получение всех продуктов."""

    stmt = select(Town).order_by(Town.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Town | None:
    """RETRIEVE - Получение продукта по id."""

    return await session.get(Town, product_id)


async def create_product(session: AsyncSession, product_in: TownCreate) -> Town:
    """CREATE - Создание продукта."""

    product = Town(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product


async def update_product(
    session: AsyncSession,
    product: Town,
    product_update: TownUpdate | TownPartialUpdate,
    partial: bool = False,
) -> Town:
    """PUT / PATCH - Обновление продукта."""

    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Town) -> Town:
    """DELETE - Удаление продукта."""

    await session.delete(product)
    await session.commit()
