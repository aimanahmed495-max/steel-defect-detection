"""FastAPI application entry point for the steel defect demo."""

from fastapi import FastAPI


app = FastAPI(title="Steel Defect Vision API")


@app.get("/")
def read_root() -> dict[str, str]:
    """Basic API metadata endpoint."""
    return {"message": "Steel Defect Vision API scaffold is ready."}


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Healthcheck endpoint for local development."""
    return {"status": "ok"}
