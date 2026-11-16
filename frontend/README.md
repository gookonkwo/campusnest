# CampusNest frontend

The first CampusNest marketplace interface is built with plain HTML, CSS and JavaScript.

## Run locally

From the repository root:

```bash
python -m http.server 5500 --directory frontend
```

Then open `http://localhost:5500`.

## Included in this first UI milestone

- Responsive marketplace homepage
- University, area and accommodation-type search
- Accommodation category shortcuts
- Listing cards with sample data, prices and details
- Price sorting
- Save/favourite interaction
- Listing detail dialog and enquiry email link
- Mobile navigation

## Important

The frontend now requests accommodation and university records from the FastAPI service at `http://127.0.0.1:8000`. If the API is unavailable, or the database has no accommodation records yet, the page clearly labels and displays its demonstration listings. Start the API from the `backend` directory with `uvicorn app.main:app --reload`, then serve the frontend from the repository root with `python3 -m http.server 5500 --directory frontend`. Open `http://localhost:5500`. The current accommodation API does not yet store listing photos or facility details, so database-backed cards use a temporary default photo and the facility filter is most useful with demo data. Login, landlord listing management and verified badges remain future work.