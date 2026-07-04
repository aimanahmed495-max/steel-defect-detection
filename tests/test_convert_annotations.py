"""Tests for VOC-to-YOLO annotation conversion helpers."""

from src.convert_annotations import CLASS_NAMES, _voc_to_yolo_bbox


def test_voc_to_yolo_bbox_centered_box() -> None:
    # 100x100 image, 20x20 box centered at (50, 50)
    x, y, w, h = _voc_to_yolo_bbox(40, 40, 60, 60, img_w=100, img_h=100)
    assert abs(x - 0.5) < 1e-6
    assert abs(y - 0.5) < 1e-6
    assert abs(w - 0.2) < 1e-6
    assert abs(h - 0.2) < 1e-6


def test_class_names_count() -> None:
    assert len(CLASS_NAMES) == 6
