from asyncio import current_task
from pathlib import Path

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "cities.sqlite3"


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

    @classmethod
    async def scoped_session_dependency(cls) -> AsyncSession:
        """Конкретная сессия, через которую будем работать с БД."""

        async with cls.get_scoped_session() as session:
            session = cls.get_scoped_session()
            yield session
            await session.close()


db_helper = DatabaseHelper(
    url=f"sqlite+aiosqlite:///{DB_PATH}",
    echo=True,
)
