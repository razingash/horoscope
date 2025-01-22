from sqlalchemy import String, Enum, SmallInteger, UniqueConstraint, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.utils import MoonEventsChoices, LanguagesChoices, MoonPhasesChoices
from core.models.base import Base

__all__ = [
    'MoonEventsSchedule', 'MoonPhases', 'MoonEvents', 'MoonEventDescription'
]
"""из-за мультиязычности создать декодеры на фронте не получится"""

class MoonEventsSchedule(Base): # in UTC
    year: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)
    month: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)

    __tablename__ = "moon_events_schedule"
    __table_args__ = (
        UniqueConstraint('year', 'month', name='idx_year_month'),
    )

    moon_phases: Mapped[list["MoonPhases"]] = relationship(
        "MoonPhases", back_populates="schedule", cascade="all, delete-orphan"
    )


class MoonPhases(Base):
    phase: Mapped[MoonPhasesChoices] = mapped_column(Enum(MoonPhasesChoices), nullable=False, index=True)
    date: Mapped[str] = mapped_column(DateTime, nullable=False, index=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("moon_events_schedule.id"), nullable=False)

    __tablename__ = "moon_phases"
    schedule: Mapped["MoonEventsSchedule"] = relationship(
        "MoonEventsSchedule", back_populates="moon_phases"
    )
    events: Mapped[list["MoonEvents"]] = relationship(
        "MoonEvents", back_populates="phase", cascade="all, delete-orphan"
    )


class MoonEvents(Base):
    event: Mapped[MoonPhasesChoices] = mapped_column(Enum(MoonPhasesChoices), nullable=False, index=True)
    phase: Mapped["MoonPhases"] = relationship("MoonPhases", back_populates="events")
    phase_id: Mapped[int] = mapped_column(ForeignKey("moon_phases.id"), nullable=False)

    __tablename__ = "moon_events"


class MoonEventDescription(Base):
    event: Mapped[MoonEventsChoices] = mapped_column(Enum(MoonEventsChoices), nullable=False, index=True)
    language: Mapped[LanguagesChoices] = mapped_column(Enum(LanguagesChoices), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    __tablename__ = "moon_event_description"
