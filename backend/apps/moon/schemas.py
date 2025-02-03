from typing import List

from pydantic import BaseModel


class MoonPhase(BaseModel):
    date: str
    phase_name: str


class MoonPhasesResponse(BaseModel):
    moon_phases: List[MoonPhase]
