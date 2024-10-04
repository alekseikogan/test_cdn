from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# class Base(DeclarativeBase):
#     __abstract__ = True

#     id: Mapped[int] = mapped_column(primary_key=True)


# class TownBase(Base):
#     title: Mapped[str]
#     latitude: Mapped[str]
#     longitude: Mapped[str]

class Town(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    latitude: Mapped[str]
    longitude: Mapped[str]
