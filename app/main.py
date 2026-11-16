from fastapi import FastAPI

app = FastAPI(
    title="CampusNest API",
    description="Backend API for the CampusNest student accommodation platform.",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return a simple status response to confirm the API is running."""
    return {"status": "ok"}
