from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Accommodation, University, User
from app.schemas.accommodation import (
    AccommodationCreate,
    AccommodationResponse,
    AccommodationUpdate,
)


router = APIRouter(prefix="/accommodations", tags=["Accommodations"])


def require_listing_manager(current_user: User) -> None:
    if current_user.role not in {"landlord", "agent"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only landlords and agents can manage accommodation listings",
        )


def get_owned_listing(
    accommodation_id: int,
    current_user: User,
    db: Session,
) -> Accommodation:
    listing = db.get(Accommodation, accommodation_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    if listing.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage your own listings",
        )
    return listing


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


@router.get("/mine", response_model=list[AccommodationResponse])
def list_my_accommodations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Accommodation]:
    """List the authenticated landlord or agent's own properties."""
    require_listing_manager(current_user)
    statement = (
        select(Accommodation)
        .where(Accommodation.owner_id == current_user.id)
        .order_by(Accommodation.created_at.desc(), Accommodation.id.desc())
    )
    return list(db.scalars(statement).all())


@router.post(
    "/",
    response_model=AccommodationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_accommodation(
    listing_data: AccommodationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Accommodation:
    """Create a listing owned by the authenticated landlord or agent."""
    require_listing_manager(current_user)

    university = db.get(University, listing_data.university_id)
    if university is None:
        raise HTTPException(status_code=404, detail="University not found")

    listing = Accommodation(
        **listing_data.model_dump(),
        owner_id=current_user.id,
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


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


@router.put("/{accommodation_id}", response_model=AccommodationResponse)
def update_accommodation(
    accommodation_id: int,
    listing_data: AccommodationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Accommodation:
    """Update a listing only when it belongs to the authenticated owner."""
    require_listing_manager(current_user)
    listing = get_owned_listing(accommodation_id, current_user, db)

    university = db.get(University, listing_data.university_id)
    if university is None:
        raise HTTPException(status_code=404, detail="University not found")

    for field, value in listing_data.model_dump().items():
        setattr(listing, field, value)

    db.commit()
    db.refresh(listing)
    return listing


@router.delete("/{accommodation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_accommodation(
    accommodation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a listing only when it belongs to the authenticated owner."""
    require_listing_manager(current_user)
    listing = get_owned_listing(accommodation_id, current_user, db)
    db.delete(listing)
    db.commit()
