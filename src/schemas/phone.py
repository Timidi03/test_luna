from pydantic import BaseModel, Field


class PhoneResponse(BaseModel):
    phone_number: str = Field(
        ..., description="Номер телефона организации", examples=["7-777-777"]
    )

    class Config:
        from_attributes = True
