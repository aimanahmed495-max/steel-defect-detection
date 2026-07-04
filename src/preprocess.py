"""Image preprocessing for steel defect detection."""

from __future__ import annotations

import cv2
import numpy as np


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: tuple[int, int] = (8, 8),
) -> np.ndarray:
    """Apply CLAHE to a BGR image to improve low-contrast defect visibility.

    Steel surface images often have subtle contrast between defects and the
    background. CLAHE operates on the L channel in LAB color space so color
    information is preserved while local contrast is boosted.

    Args:
        image: Input image in BGR format (OpenCV convention).
        clip_limit: Threshold for contrast limiting; higher values allow more
            contrast amplification.
        tile_grid_size: Grid size for adaptive histogram equalization.

    Returns:
        Preprocessed BGR image with the same shape as the input.
    """
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(f"Expected a 3-channel BGR image, got shape {image.shape}")

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    l_enhanced = clahe.apply(l_channel)

    merged = cv2.merge([l_enhanced, a_channel, b_channel])
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def preprocess_for_detection(image: np.ndarray) -> np.ndarray:
    """Run the full preprocessing chain before YOLO inference."""
    return apply_clahe(image)
