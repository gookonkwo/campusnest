# CampusNest Backend

The CampusNest backend is built with Python and FastAPI.

## Run locally

From the `backend` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open these addresses after the server starts:

- API welcome: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

## Current scope

This is the initial API foundation. Authentication, database integration, accommodation listings, search, and booking requests will be added in later milestones.
