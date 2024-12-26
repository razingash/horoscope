from sqlalchemy import String, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.utils import LanguagesChoices, MoonEventsChoices


class MoonEventsSchedule(Base):
    """in UTC"""

    date: Mapped[str] = mapped_column(Date, unique=True, index=True)
    path: Mapped[str] = mapped_column(String(150), nullable=False)

    __tablename__ = "moon_events_schedule"


class MoonEventDescription(Base):
    event: Mapped[MoonEventsChoices] = mapped_column(Enum(MoonEventsChoices), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    language: Mapped[LanguagesChoices] = mapped_column(Enum(LanguagesChoices), nullable=False)

    __tablename__ = "moon_event_description"
