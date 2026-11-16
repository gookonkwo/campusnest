from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import University


def make_test_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    test_session = sessionmaker(bind=engine)
    return test_session()


def test_can_save_and_read_a_university():
    db = make_test_session()
    university = University(
        name="University of Nigeria, Nsukka",
        slug="university-of-nigeria-nsukka",
        state="Enugu",
        institution_type="federal",
    )

    db.add(university)
    db.commit()

    saved = db.query(University).filter_by(slug="university-of-nigeria-nsukka").first()

    assert saved is not None
    assert saved.name == "University of Nigeria, Nsukka"
    assert saved.state == "Enugu"
    assert saved.institution_type == "federal"

    db.close()
