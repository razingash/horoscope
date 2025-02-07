from datetime import date

from sqlalchemy import Text, Date
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class SolarSystemMap(Base):
    text_data: Mapped[str] = mapped_column(Text, nullable=False)
    last_date: Mapped[date] = mapped_column(Date, nullable=False, index=True, unique=True)

    __tablename__ = "solar_system_map"
