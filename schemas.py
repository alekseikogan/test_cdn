from pydantic import BaseModel


class Town(BaseModel):
    """Модель города."""
    id: int
    title: str  # название города
    latitude: str  # широта
    longitude: str  # долгота


class TownCreate(Town):
    """Добавление города в БД."""

    pass
