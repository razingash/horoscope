from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String, primary_key=True)

    __abstract__ = True
