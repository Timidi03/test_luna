from typing import List

from pydantic import BaseModel, Field

from src.core.constants import (
    MAX_LAT,
    MAX_LENGTH_STRING,
    MAX_LON,
    MIN_ID,
    MIN_LAT,
    MIN_LENGTH_STRING,
    MIN_LON,
)
from src.schemas.activity import ActivityResponse
from src.schemas.building import BuildingResponse
from src.schemas.phone import PhoneResponse


class OrganizationResponse(BaseModel):
    id: int = Field(
        ..., ge=MIN_ID, description="Уникальный идентификатор организации", examples=[1]
    )
    name: str = Field(
        ...,
        min_length=MIN_LENGTH_STRING,
        max_length=MAX_LENGTH_STRING,
        description="Название организации",
        examples=["OOO TechSot"],
    )
    phones: List[PhoneResponse] = Field(
        ...,
        description="Список номеров телефонов организации (хотя бы один номер)",
    )
    activities: List[ActivityResponse] = Field(
        ...,
        description="Список видов деятельности организации (хотя бы один)",
    )
    building: BuildingResponse = Field(
        ..., description="Информация о здании организации"
    )

    class Config:
        from_attributes = True


class OrganizationBox(BaseModel):
    lat_min: float = Field(
        ..., ge=MIN_LAT, le=MAX_LAT, description="Минимальная широта (x0)"
    )
    lon_min: float = Field(
        ..., ge=MIN_LON, le=MAX_LON, description="Минимальная долгота (y0)"
    )
    lat_max: float = Field(
        ..., ge=MIN_LAT, le=MAX_LAT, description="Максимальная широта (x1)"
    )
    lon_max: float = Field(
        ..., ge=MIN_LON, le=MAX_LON, description="Максимальная долгота (y1)"
    )
