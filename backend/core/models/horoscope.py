from sqlalchemy import Enum, String, SmallInteger, UniqueConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base, PlanetsChoices, ZodiacsChoices, LanguagesChoices, HousesChoices, AspectsChoices, \
    HoroscopeTypes

__all__ = [
    'PlanetPatterns', 'AspectPatterns', 'HousePatterns', 'HoroscopePatterns', 'Horoscope'
]

"""
надо будет прокачать всю систему тут, потому что если объединить всю систему то скорее всего можно будет нормализовать
базу данных, скорее всего уменьшится количество запросов к паттернам
"""

class PlanetPatterns(Base): # used for natal chart description
    __tablename__ = "planet_patterns"
    planet: Mapped[PlanetsChoices] = mapped_column(Enum(PlanetsChoices), nullable=False, index=True)
    language: Mapped[LanguagesChoices] = mapped_column(Enum(LanguagesChoices), nullable=False, index=True)
    zodiac: Mapped[ZodiacsChoices] = mapped_column(Enum(ZodiacsChoices), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)


class AspectPatterns(Base): # used for natal chart description
    __tablename__ = "aspect_patterns"
    planet: Mapped[PlanetsChoices] = mapped_column(Enum(PlanetsChoices), nullable=False, index=True)
    language: Mapped[LanguagesChoices] = mapped_column(Enum(LanguagesChoices), nullable=False, index=True)
    aspect: Mapped[AspectsChoices] = mapped_column(Enum(AspectsChoices), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)


class HousePatterns(Base): # used for natal chart description
    __tablename__ = "house_patterns"
    planet: Mapped[PlanetsChoices] = mapped_column(Enum(PlanetsChoices), nullable=False, index=True)
    language: Mapped[LanguagesChoices] = mapped_column(Enum(LanguagesChoices), nullable=False, index=True)
    house: Mapped[HousesChoices] = mapped_column(Enum(HousesChoices), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)


class HoroscopePatterns(Base):
    __tablename__ = "horoscope_patterns"
    type: Mapped[HoroscopeTypes] = mapped_column(SmallInteger, nullable=False, index=True)
    planet: Mapped[PlanetsChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    language: Mapped[LanguagesChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    house: Mapped[HousesChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    zodiac: Mapped[ZodiacsChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    aspect: Mapped[AspectsChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)


class Horoscope(Base):
    type: Mapped[HoroscopeTypes] = mapped_column(Enum(HoroscopeTypes), nullable=False, index=True)
    date: Mapped[str] = mapped_column(Date, nullable=False, index=True)
    path: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    __tablename__ = "horoscope"
    __table_args__ = (
        UniqueConstraint('type', 'date', name='idx_year_month'),
    )
