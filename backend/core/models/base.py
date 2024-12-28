from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)

    __abstract__ = True
