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

The FastAPI backend, university and accommodation APIs, database migrations, and first responsive marketplace frontend are available on the `feat/fastapi-foundation` branch.

### Frontend

The first CampusNest marketplace interface is in `frontend/`. It includes a responsive home page, campus and area search, accommodation categories, sample listing cards, price sorting, favourites, and listing detail dialogs. The visual identity uses deep navy, teal, and warm off-white. The listings are currently demo data; live API integration, accounts, enquiries, and landlord tools are planned next.

Run the frontend locally from the repository root with:

```bash
python -m http.server 5500 --directory frontend
```

Then visit `http://localhost:5500`. See [frontend/README.md](frontend/README.md) for details.

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

1. Add student, landlord, and agent accounts with authentication.
2. Connect the frontend search and listing cards to the FastAPI endpoints.
3. Add secure landlord listing creation and management.
4. Add enquiries, booking requests, moderation, and reporting tools.
5. Add image uploads and verified listing workflows.
