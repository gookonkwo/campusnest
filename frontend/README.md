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

The current listings are demonstration data stored in `app.js`. Search, filters, sorting, favourites and listing details work in the browser, but the frontend is not yet connected to the FastAPI database. Login, live enquiries, landlord listing management and verified badges will be connected as their backend features are built.