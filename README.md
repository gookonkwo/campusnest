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

The initial FastAPI backend foundation is available on the `feat/fastapi-foundation` branch.

### Backend endpoints

- `GET /` — API welcome message
- `GET /health` — basic health check
- `GET /docs` — interactive API documentation (provided by FastAPI)

See [backend/README.md](backend/README.md) for local setup instructions.

### Planned next milestones

1. Add automated tests and backend quality checks.
2. Connect PostgreSQL.
3. Design the university, user, landlord, and accommodation data models.
4. Add authentication and role-based permissions.
5. Build accommodation listing and search features.
6. Add enquiries and booking requests.
7. Add listing moderation and reporting tools.
