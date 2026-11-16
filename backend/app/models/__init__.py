"""SQLAlchemy models used by the CampusNest API."""

from app.models.accommodation import Accommodation
from app.models.university import University
from app.models.user import User

__all__ = ["Accommodation", "University", "User"]
