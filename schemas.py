from pydantic import BaseModel


class City(BaseModel):
    """Модель города."""
    id: int
    title: str  # название города
    latitude: str  # широта
    longitude: str  # долгота


class CityCreate(City):
    """Добавление города в БД."""

    pass