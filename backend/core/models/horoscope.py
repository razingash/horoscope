from sqlalchemy import Enum, String, SmallInteger, UniqueConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column, validates

from core.models.base import Base, HoroscopePreciseBase, HoroscopeVoidBase, HoroscopeBase, HoroscopeCompleteBase
from core.models.utils import ZodiacsChoices, AspectsChoices, HoroscopeTypes, MoonPhasesChoices, EarthSeasons

__all__ = [
    'HoroscopeFitDaily', 'HoroscopeVoidDaily', 'HoroscopeFitWeekly', 'HoroscopeVoidWeekly', 'HoroscopeFitMonthly',
    'HoroscopeVoidMonthly', 'HoroscopeFitAnnual', 'HoroscopeVoidAnnual', 'Horoscope', 'HoroscopeDaily',
    'HoroscopeWeekly', 'HoroscopeMonthly', 'HoroscopeAnnual'
]


class HoroscopeFitDaily(HoroscopePreciseBase):
    aspect: Mapped[AspectsChoices] = mapped_column(SmallInteger, nullable=False, index=True)

    __tablename__ = "horoscope_daily_fit"
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'house', 'planet', 'aspect',
                         name='idx_language_zodiac_house_planet_aspect'),
    )


class HoroscopeVoidDaily(HoroscopeBase):
    zodiac: Mapped[ZodiacsChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    moon_position: Mapped[ZodiacsChoices] = mapped_column(SmallInteger, nullable=False, index=True)
    moon_cycle: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)

    __tablename__ = "horoscope_daily_void"
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'moon_position', 'moon_cycle',
                         name='idx_language_zodiac_moon_position_moon_cycle'),
    )

    @validates('moon_cycle')
    def validate_moon_cycle(self, key, value):
        if not (1 <= value <= 30):
            raise ValueError("moon_cycle must be between 1 and 30")
        return value


class HoroscopeFitWeekly(HoroscopePreciseBase):
    lunar_phase: Mapped[MoonPhasesChoices] = mapped_column(SmallInteger, nullable=False, index=True)

    __tablename__ = "horoscope_weekly_fit"
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'house', 'planet', 'lunar_phase',
                         name='idx_language_zodiac_house_planet_lunar_phase'),
    )


class HoroscopeVoidWeekly(HoroscopeVoidBase):
    lunar_phase: Mapped[MoonPhasesChoices] = mapped_column(SmallInteger, nullable=False, index=True)

    __tablename__ = "horoscope_weekly_void"
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'house', 'main_planet_position', 'lunar_phase',
                         name='idx_language_zodiac_house_planet_lunar_phase'),
    )


class HoroscopeFitMonthly(HoroscopePreciseBase):
    season: Mapped[EarthSeasons] = mapped_column(SmallInteger, nullable=False, index=True)

    __tablename__ = "horoscope_monthly_fit"
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'house', 'planet', 'season',
                         name='idx_language_zodiac_house_planet_season'),
    )


class HoroscopeVoidMonthly(HoroscopeVoidBase):
    __tablename__ = "horoscope_monthly_void"


class HoroscopeFitAnnual(HoroscopePreciseBase):
    __tablename__ = "horoscope_annual_fit"


class HoroscopeVoidAnnual(HoroscopeVoidBase):
    __tablename__ = "horoscope_annual_void"


class HoroscopeDaily(HoroscopeCompleteBase):
    day: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)
    month: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)

    __tablename__ = "horoscope_daily"
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'year', 'month', 'day', name='idx_language_zodiac_year_month_day'),
    )


class HoroscopeWeekly(HoroscopeCompleteBase):
    week_number: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)
    month: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)

    __tablename__ = "horoscope_weekly"
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'year', 'month', 'week_number',
                         name='idx_language_zodiac_year_month_week_number'),
    )


class HoroscopeMonthly(HoroscopeCompleteBase):
    month: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)

    __tablename__ = "horoscope_monthly"
    __table_args__ = (
        UniqueConstraint('language', 'zodiac', 'year', 'month', name='idx_language_zodiac_year_month'),
    )


class HoroscopeAnnual(HoroscopeCompleteBase):
    __tablename__ = "horoscope_annual"


class Horoscope(Base): # существует для хранения пути к json данным
    type: Mapped[HoroscopeTypes] = mapped_column(Enum(HoroscopeTypes), nullable=False, index=True)
    date: Mapped[str] = mapped_column(Date, nullable=False, index=True)
    path: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    __tablename__ = "horoscope" # rename?
    __table_args__ = (
        UniqueConstraint('type', 'date', name='idx_year_month'),
    )
