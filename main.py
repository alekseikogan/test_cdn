from typing import List
from fastapi import Depends, FastAPI
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

import db_helper
from models import Town

app = FastAPI(
    title="Distance between cities",
)


@app.get("", response_model=List[Town])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """GET - Получение всех продуктов."""

    stmt = select(Town).order_by(Town.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()

    return list(products)


@app.get("/{product_id}", response_model=Town)
async def get_product(product: Town = Depends(product_by_id)) -> Town:
    """RETRIEVE - Получение продукта по id."""

    return product


@router.post("", response_model=Town)
async def create_product(
    product_in: TownCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """CREATE - Создание продукта."""

    return await crud.create_product(session=session, product_in=product_in)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)