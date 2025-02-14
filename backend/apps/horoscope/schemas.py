from datetime import datetime, timezone

from fastapi import Query
from pydantic import BaseModel, field_validator

from core.models import LanguagesChoices

MIN_DATE = datetime(1549, 12, 31, tzinfo=timezone.utc)
MAX_DATE = datetime(2650, 1, 25, tzinfo=timezone.utc)


class HoroscopeQueryParams(BaseModel):
    date: datetime = Query(default=datetime.now(timezone.utc))
    language: LanguagesChoices = Query(default=LanguagesChoices.ENGLISH)

    @field_validator('date')
    def validate_date(cls, value: datetime) -> datetime:
        if not (MIN_DATE <= value <= MAX_DATE):
            return datetime.now(timezone.utc)
        return value
