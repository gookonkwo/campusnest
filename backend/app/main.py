from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import accommodations, universities

app = FastAPI(
    title="CampusNest API",
    description="API for discovering and managing student accommodation.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
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
