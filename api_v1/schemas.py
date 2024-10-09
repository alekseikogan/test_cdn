from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    """Основа модели города."""
    name: str
    latitude: float
    longitude: float


class City(CityBase):
    """Модель города для возврата данных."""

    model_config = ConfigDict(from_attributes=True)
    id: int


class CityCreate(City):
    """Добавление города в БД."""

    name: str
