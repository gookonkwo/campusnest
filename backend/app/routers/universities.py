from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import University
from app.schemas.university import UniversityResponse


router = APIRouter(prefix="/universities", tags=["Universities"])


@router.get("/", response_model=list[UniversityResponse])
def list_universities(
    state: str | None = None,
    institution_type: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[University]:
    """List universities, with optional filters and pagination."""
    statement = select(University)

    if state:
        statement = statement.where(University.state.ilike(state))

    if institution_type:
        statement = statement.where(
            University.institution_type.ilike(institution_type)
        )

    statement = statement.order_by(University.name).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


@router.get("/{university_id}", response_model=UniversityResponse)
def get_university(
    university_id: int,
    db: Session = Depends(get_db),
) -> University:
    """Return one university by its database ID."""
    university = db.get(University, university_id)

    if university is None:
        raise HTTPException(status_code=404, detail="University not found")

    return university
