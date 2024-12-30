from __future__ import annotations

from datetime import datetime

from sqlmodel import SQLModel, Field


class TripRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    origin: str = Field()
    destination: str = Field()
    accepted: bool | None = Field(default=False)
    trip_time: datetime | None = Field(default_factory=lambda: datetime.now())




