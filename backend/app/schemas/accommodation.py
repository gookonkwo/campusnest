from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


AccommodationType = Literal[
    "school_hostel",
    "private_hostel",
    "self_contained",
    "shared_apartment",
    "single_room",
    "self_contained_room",
]
PricePeriod = Literal["weekly", "monthly", "semester", "yearly"]


class AccommodationCreate(BaseModel):
    title: str = Field(min_length=5, max_length=180)
    description: str = Field(min_length=20, max_length=5000)
    accommodation_type: AccommodationType
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    price_period: PricePeriod
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
