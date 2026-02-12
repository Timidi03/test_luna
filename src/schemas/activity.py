from pydantic import BaseModel, Field

from src.core.constants import MAX_LENGTH_STRING, MIN_LENGTH_STRING


class ActivityResponse(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_LENGTH_STRING,
        max_length=MAX_LENGTH_STRING,
        description="Название деятельности организации",
        examples=["Мясная продукция"],
    )

    class Config:
        from_attributes = True
