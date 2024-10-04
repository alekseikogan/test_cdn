from pydantic import BaseModel, ConfigDict


class TownBase(BaseModel):
    """Модель города."""
    id: int
    title: str  # название города
    latitude: int  # широта
    longitude: str  # долгота


class TownCreate(TownBase):
    """Добавление города в БД."""

    pass
