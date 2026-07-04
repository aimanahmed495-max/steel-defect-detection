"""Tests for CLAHE preprocessing."""

import numpy as np

from src.preprocess import apply_clahe, preprocess_for_detection


def test_apply_clahe_preserves_shape() -> None:
    image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    result = apply_clahe(image)
    assert result.shape == image.shape
    assert result.dtype == np.uint8


def test_preprocess_for_detection_delegates_to_clahe() -> None:
    image = np.full((64, 64, 3), 128, dtype=np.uint8)
    result = preprocess_for_detection(image)
    assert result.shape == image.shape
