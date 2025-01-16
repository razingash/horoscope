from sqlalchemy import String, Enum, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.models.utils import MoonEventsChoices, LanguagesChoices
from core.models.base import Base

__all__ = [
    'MoonEventsSchedule', 'MoonEventDescription'
]
"""из-за мультиязычности создать декодеры на фронте не получится"""

class MoonEventsSchedule(Base): # in UTC
    year: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    month: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    path: Mapped[str] = mapped_column(String(150), nullable=False)

    __tablename__ = "moon_events_schedule"
    __table_args__ = (
        UniqueConstraint('year', 'month', name='idx_year_month'),
    )


class MoonEventDescription(Base):
    event: Mapped[MoonEventsChoices] = mapped_column(Enum(MoonEventsChoices), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    language: Mapped[LanguagesChoices] = mapped_column(Enum(LanguagesChoices), nullable=False)

    __tablename__ = "moon_event_description"
