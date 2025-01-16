from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, SmallInteger, String, UniqueConstraint, Enum

from core.models.utils import HousesChoices, PlanetsChoices, ZodiacsChoices, LanguagesChoices  # циркулярка


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)

    __abstract__ = True


class HoroscopeBase(Base):
    language: Mapped[LanguagesChoices] = mapped_column(Enum(LanguagesChoices), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)

    __abstract__ = True


class HoroscopePreciseBase(HoroscopeBase):
    """Used as parent for all "precise" combinations except daily dead type"""
    zodiac: Mapped[ZodiacsChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    planet: Mapped[PlanetsChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    house: Mapped[HousesChoices] = mapped_column(SmallInteger, nullable=False, index=True)

    __abstract__ = True
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'house', 'planet',
                         name='idx_language_zodiac_house_planet'),
    )


class HoroscopeVoidBase(HoroscopeBase):
    """Used as parent for all "precise" combinations except daily dead type"""
    zodiac: Mapped[ZodiacsChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    house: Mapped[HousesChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    main_planet_position: Mapped[ZodiacsChoices] = mapped_column(SmallInteger, nullable=False, index=True)

    __abstract__ = True
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'house', 'main_planet_position',
                         name='idx_language_zodiac_house_planet_position'),
    )

