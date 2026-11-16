from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Accommodation
from app.schemas.accommodation import AccommodationResponse


router = APIRouter(prefix="/accommodations", tags=["Accommodations"])


@router.get("/", response_model=list[AccommodationResponse])
def list_accommodations(
    university_id: int | None = Query(default=None, ge=1),
    accommodation_type: str | None = None,
    area: str | None = None,
    min_price: Decimal | None = Query(default=None, gt=0),
    max_price: Decimal | None = Query(default=None, gt=0),
    available_only: bool = True,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[Accommodation]:
    """List accommodation options with optional filters and pagination."""
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=422,
            detail="min_price cannot be greater than max_price",
        )

    statement = select(Accommodation)

    if university_id is not None:
        statement = statement.where(Accommodation.university_id == university_id)

    if accommodation_type:
        statement = statement.where(
            Accommodation.accommodation_type.ilike(accommodation_type)
        )

    if area:
        statement = statement.where(Accommodation.area.ilike(area))

    if min_price is not None:
        statement = statement.where(Accommodation.price >= min_price)

    if max_price is not None:
        statement = statement.where(Accommodation.price <= max_price)

    if available_only:
        statement = statement.where(Accommodation.is_available.is_(True))

    statement = (
        statement.order_by(Accommodation.created_at.desc(), Accommodation.id.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


@router.get("/{accommodation_id}", response_model=AccommodationResponse)
def get_accommodation(
    accommodation_id: int,
    db: Session = Depends(get_db),
) -> Accommodation:
    """Return one accommodation listing by its database ID."""
    accommodation = db.get(Accommodation, accommodation_id)

    if accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")

    return accommodation
