"""Vision-language model wrapper for defect report generation."""

from dataclasses import dataclass


@dataclass
class DefectReport:
    """Structured report returned by the VLM layer."""

    description: str
    severity: str
    recommended_action: str


def generate_report(image_bytes: bytes, defect_label: str) -> DefectReport:
    """Generate a natural-language report for a detected defect."""
    raise NotImplementedError("VLM integration is not implemented yet.")
