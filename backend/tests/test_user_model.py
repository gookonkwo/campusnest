from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import User


def make_test_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    test_session = sessionmaker(bind=engine)
    return test_session()


def test_can_save_and_read_a_user():
    db = make_test_session()
    user = User(
        full_name="Ada Student",
        email="ada@example.com",
        hashed_password="a-secure-hash",
        role="student",
    )

    db.add(user)
    db.commit()

    saved = db.query(User).filter_by(email="ada@example.com").first()

    assert saved is not None
    assert saved.full_name == "Ada Student"
    assert saved.role == "student"
    assert saved.is_active is True
    assert saved.hashed_password == "a-secure-hash"

    db.close()
