from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from . import crud
from ..dependencies import product_by_id
from .schemas import Town, TownCreate, TownPartialUpdate, TownUpdate

router = APIRouter(
    prefix="/products",
    tags=["Towns"],
)


@router.get("", response_model=List[Town])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """GET - Получение всех продуктов."""

    return await crud.get_products(session=session)


@router.get("/{product_id}", response_model=Town)
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


@router.put("/{product_id}")
async def update_product(
    product_update: TownUpdate,
    product: Town = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """PUT - Обновление продукта."""

    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}")
async def partial_update_product(
    product_update: TownPartialUpdate,
    product: Town = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """PATCH - Частичное обновление продукта."""

    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete("/{product_id}")
async def delete_product(
    product: Town = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """DELETE - Удаление продукта."""

    await crud.delete_product(session=session, product=product)
    return {
        "success": True,
        "message": f"Продукт id={product.id} {product.name} успешно удален!",
    }
