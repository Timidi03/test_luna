from pydantic import BaseModel, Field

from src.core.constants import (
    MAX_LAT,
    MAX_LENGTH_STRING,
    MAX_LON,
    MIN_LAT,
    MIN_LENGTH_STRING,
    MIN_LON,
)


class BuildingResponse(BaseModel):
    address: str = Field(
        ...,
        min_length=MIN_LENGTH_STRING,
        max_length=MAX_LENGTH_STRING,
        description="Address",
        examples=["г. Москва, ул. Ленина 1"],
    )
    latitude: float = Field(
        ..., ge=MIN_LAT, le=MAX_LAT, description="Latitude", examples=["45.123456"]
    )
    longitude: float = Field(
        ..., ge=MIN_LON, le=MAX_LON, description="Longitude", examples=["55.123456"]
    )

    class Config:
        from_attributes = True
