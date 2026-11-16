# CampusNest

**Find Your Space. Feel at Home.**

CampusNest is a student accommodation discovery platform starting with universities and other higher institutions across Nigeria, with room for future international expansion.

## Project direction

CampusNest will help students discover and compare genuine accommodation, contact landlords or agents, and submit booking requests. Landlords and agents will be able to manage property listings, while administrators will review listings and reports.

### Accommodation types

- School and private hostels
- Self-contained apartments and rooms
- Shared apartments
- Single rooms

## Planned technology

- Backend: Python with FastAPI
- Database: PostgreSQL
- Frontend: HTML, CSS, and JavaScript
- Version control: Git and GitHub

## Development approach

The project will be built in small, testable stages. Each stage should be understandable, testable, and reviewed before it is merged into `main`.

## Current status

The initial FastAPI backend and first database foundation are available on the `feat/fastapi-foundation` branch.

### Backend endpoints

- `GET /` — API welcome message
- `GET /health` — basic health check
- `GET /docs` — interactive API documentation (provided by FastAPI)

See [backend/README.md](backend/README.md) for local setup instructions.

### Database foundation

- SQLAlchemy is configured as the ORM.
- PostgreSQL support is included through the Psycopg driver.
- A `University` model is defined with a unique name and slug, state, institution type, and creation timestamp.
- Local development and automated tests can use SQLite; PostgreSQL is the intended production database.
- Database credentials are supplied through the `DATABASE_URL` environment variable. Do not commit real credentials.

### Planned next milestones

1. Verify the database model tests in GitHub Actions.
2. Add database migrations with Alembic.
3. Add university API endpoints and validation.
4. Design user, landlord, and accommodation data models.
5. Add authentication and role-based permissions.
6. Build accommodation listing and search features.
7. Add enquiries, booking requests, moderation, and reporting tools.
