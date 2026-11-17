# CampusNest Backend

The CampusNest backend is built with Python and FastAPI.

## Run locally

From the backend directory:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    alembic upgrade head
    uvicorn app.main:app --reload

Open the API documentation at http://127.0.0.1:8000/docs. The frontend can call this API from http://localhost:5500 or http://127.0.0.1:5500 during local development.

## Authentication

The API supports email-and-password registration and login.

- POST /auth/register creates a student, landlord, or agent account.
- POST /auth/login checks the email and password and returns a bearer token.
- GET /auth/me returns the signed-in user's profile and requires an Authorization: Bearer <token> header.

Passwords must contain at least eight characters and are stored as secure hashes, never as plain text. Email addresses are normalized to lowercase. Public registration cannot create admin accounts.

Access tokens expire after 30 minutes. Set a strong, private JWT_SECRET_KEY environment variable before deploying. The built-in fallback key is only for local development and must not be used in production. Keep secrets out of Git.

Example registration JSON:

    {
      "full_name": "Ada Student",
      "email": "ada@example.com",
      "password": "a-strong-password",
      "role": "student"
    }

Allowed public roles are student, landlord, and agent. The role defaults to student when omitted.

## Current scope

The API includes health checks, read-only university and accommodation endpoints, and user registration/login. Accommodation results can be filtered by university, accommodation type, area, price range, and availability, with pagination. Listings must belong to a registered university and must have a positive price. Public listing creation is not yet available; landlord-only listing management is the next milestone.

## Database setup

The backend uses SQLAlchemy and PostgreSQL. Set the DATABASE_URL environment variable before starting the API. For local development, SQLite is used if no URL is supplied.

Example PostgreSQL URL:

    postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE

Do not commit database credentials or place real passwords in source files.

## Database migrations

From the backend directory, activate your virtual environment and run:

    alembic upgrade head

The existing users migration creates the table used by registration and login. No new database migration is required for this authentication milestone.
