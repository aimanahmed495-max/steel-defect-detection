"""FastAPI application entry point for the steel defect demo."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="Steel Defect Vision API")


@app.get("/api")
def read_api_metadata() -> dict[str, str]:
    """Basic API metadata endpoint."""
    return {"message": "Steel Defect Vision API scaffold is ready."}


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Healthcheck endpoint for local development."""
    return {"status": "ok"}


if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
