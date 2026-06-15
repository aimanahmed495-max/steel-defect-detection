"""Inference pipeline for steel defect detection and reporting."""

from dataclasses import dataclass
from typing import Any


@dataclass
class DetectionResult:
    """Single defect detection produced by the detector."""

    label: str
    confidence: float
    bbox: tuple[int, int, int, int]


def run_pipeline(image: Any) -> dict[str, Any]:
    """Run preprocessing, detection, post-processing, and VLM analysis."""
    raise NotImplementedError("Inference pipeline is not implemented yet.")
