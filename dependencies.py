from typing import Annotated
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import Town
from .models import db_helper
from .api_v1 import crud


async def product_by_id(
    town_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Town:
    """Получение продукта по id."""

    town = await crud.get_product(session=session, town_id=town_id)
    if town is not None:
        return town
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Продукт {town_id} не найден!'
    )
