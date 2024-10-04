from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Distance between cities",
)


@app.get("", response_model=List[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """GET - Получение всех продуктов."""

    return await crud.get_products(session=session)


@app.get("/{product_id}", response_model=Product)
async def get_product(product: Product = Depends(product_by_id)) -> Product:
    """RETRIEVE - Получение продукта по id."""

    return product


@router.post("", response_model=Product)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """CREATE - Создание продукта."""

    return await crud.create_product(session=session, product_in=product_in)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)