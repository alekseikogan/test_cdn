from asyncio import current_task

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)

from .config import settings

from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "shop_db.sqlite3"


class Settings(BaseSettings):
    """Для подгрузки переменных окружения."""

    url: str = f"sqlite+aiosqlite:///{DB_PATH}"


settings = Settings()

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        # создание движка
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # создает новую сессию при каждом вызове
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """Создает сессию и связывает ее с текущим потоком выполнения (scope)."""

        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def scoped_session_dependency(self) -> AsyncSession:
        """Конкретная сессия, через которую будем рабоать с БД."""

        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo
)
