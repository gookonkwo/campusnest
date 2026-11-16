from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


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
    is_available: bool
    created_at: datetime
