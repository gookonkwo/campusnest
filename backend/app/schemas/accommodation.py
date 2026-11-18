from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AccommodationCreate(BaseModel):
    title: str = Field(min_length=5, max_length=180)
    description: str = Field(min_length=20, max_length=5000)
    accommodation_type: str = Field(min_length=3, max_length=40)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    price_period: str = Field(min_length=3, max_length=20)
    area: str = Field(min_length=2, max_length=120)
    address: str = Field(min_length=5, max_length=255)
    university_id: int = Field(gt=0)


class AccommodationUpdate(AccommodationCreate):
    is_available: bool = True


class AccommodationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    accommodation_type: str
    price: Decimal
    price_period: str
    area: str
    address: str
    university_id: int
    owner_id: int | None
    is_available: bool
    created_at: datetime
