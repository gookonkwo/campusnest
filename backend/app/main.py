from fastapi import FastAPI

from app.routers import accommodations, universities

app = FastAPI(
    title="CampusNest API",
    description="API for discovering and managing student accommodation.",
    version="0.1.0",
)

app.include_router(universities.router)
app.include_router(accommodations.router)


@app.get("/", tags=["General"])
async def read_root() -> dict[str, str]:
    return {
        "message": "Welcome to CampusNest API",
        "status": "running",
    }


@app.get("/health", tags=["General"])
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
