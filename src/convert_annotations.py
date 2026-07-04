"""Convert NEU-DET VOC annotations into YOLO format."""

from __future__ import annotations

import argparse
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


RAW_DATASET_DIR = Path("data/NEU-DET")
OUTPUT_DIR = Path("data/yolo")

CLASS_NAMES: tuple[str, ...] = (
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches",
)
CLASS_TO_ID: dict[str, int] = {name: idx for idx, name in enumerate(CLASS_NAMES)}

# NEU-DET ships a `validation` folder; YOLO config conventionally calls it `val`.
SPLIT_MAP: dict[str, str] = {"train": "train", "validation": "val"}


def _voc_to_yolo_bbox(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    img_w: int,
    img_h: int,
) -> tuple[float, float, float, float]:
    x_center = ((xmin + xmax) / 2) / img_w
    y_center = ((ymin + ymax) / 2) / img_h
    width = (xmax - xmin) / img_w
    height = (ymax - ymin) / img_h
    return x_center, y_center, width, height


def _parse_voc(xml_path: Path) -> list[tuple[int, float, float, float, float]]:
    """Return a list of (class_id, x_center, y_center, w, h) tuples in YOLO format."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    if size is None:
        raise ValueError(f"{xml_path}: missing <size> element")
    img_w = int(size.findtext("width", "0"))
    img_h = int(size.findtext("height", "0"))
    if img_w <= 0 or img_h <= 0:
        raise ValueError(f"{xml_path}: invalid image size {img_w}x{img_h}")

    boxes: list[tuple[int, float, float, float, float]] = []
    for obj in root.findall("object"):
        name = (obj.findtext("name") or "").strip()
        if name not in CLASS_TO_ID:
            raise ValueError(f"{xml_path}: unknown class '{name}'")

        bnd = obj.find("bndbox")
        if bnd is None:
            raise ValueError(f"{xml_path}: object '{name}' missing <bndbox>")

        xmin = float(bnd.findtext("xmin", "0"))
        ymin = float(bnd.findtext("ymin", "0"))
        xmax = float(bnd.findtext("xmax", "0"))
        ymax = float(bnd.findtext("ymax", "0"))

        # Some NEU-DET boxes touch or slightly exceed the image border; clamp to be safe.
        xmin = max(0.0, min(xmin, float(img_w)))
        xmax = max(0.0, min(xmax, float(img_w)))
        ymin = max(0.0, min(ymin, float(img_h)))
        ymax = max(0.0, min(ymax, float(img_h)))
        if xmax <= xmin or ymax <= ymin:
            continue

        cls_id = CLASS_TO_ID[name]
        x, y, w, h = _voc_to_yolo_bbox(xmin, ymin, xmax, ymax, img_w, img_h)
        boxes.append((cls_id, x, y, w, h))

    return boxes


def _find_image(images_root: Path, stem: str) -> Path | None:
    """Locate the .jpg matching an annotation stem inside class-named subfolders."""
    for class_name in CLASS_NAMES:
        if stem.startswith(class_name + "_"):
            candidate = images_root / class_name / f"{stem}.jpg"
            if candidate.is_file():
                return candidate
            break

    for class_dir in images_root.iterdir():
        if class_dir.is_dir():
            candidate = class_dir / f"{stem}.jpg"
            if candidate.is_file():
                return candidate
    return None


def _convert_split(
    raw_dataset_dir: Path,
    output_dir: Path,
    src_split: str,
    dst_split: str,
) -> int:
    annotations_dir = raw_dataset_dir / src_split / "annotations"
    images_dir = raw_dataset_dir / src_split / "images"

    if not annotations_dir.is_dir():
        raise FileNotFoundError(f"Annotations folder not found: {annotations_dir}")
    if not images_dir.is_dir():
        raise FileNotFoundError(f"Images folder not found: {images_dir}")

    out_images = output_dir / "images" / dst_split
    out_labels = output_dir / "labels" / dst_split
    out_images.mkdir(parents=True, exist_ok=True)
    out_labels.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    for xml_path in sorted(annotations_dir.glob("*.xml")):
        stem = xml_path.stem
        image_path = _find_image(images_dir, stem)
        if image_path is None:
            print(f"  WARN: no image found for {xml_path.name}, skipping")
            skipped += 1
            continue

        boxes = _parse_voc(xml_path)

        label_path = out_labels / f"{stem}.txt"
        with label_path.open("w", encoding="utf-8") as f:
            for cls_id, x, y, w, h in boxes:
                f.write(f"{cls_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

        dst_image = out_images / image_path.name
        if not dst_image.exists():
            shutil.copy2(image_path, dst_image)

        written += 1

    if skipped:
        print(f"  Skipped {skipped} annotation(s) with no matching image")
    return written


def _write_data_yaml(output_dir: Path) -> Path:
    yaml_path = output_dir / "data.yaml"
    abs_out = output_dir.resolve()
    lines = [
        f"path: {abs_out.as_posix()}",
        "train: images/train",
        "val: images/val",
        "",
        "names:",
    ]
    for idx, name in enumerate(CLASS_NAMES):
        lines.append(f"  {idx}: {name}")
    yaml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return yaml_path


def convert_dataset(
    raw_dataset_dir: Path = RAW_DATASET_DIR,
    output_dir: Path = OUTPUT_DIR,
) -> None:
    """Convert XML annotations and images into a YOLO-friendly layout."""
    if not raw_dataset_dir.is_dir():
        raise FileNotFoundError(f"Raw dataset not found at: {raw_dataset_dir.resolve()}")

    print(f"Source : {raw_dataset_dir.resolve()}")
    print(f"Target : {output_dir.resolve()}")
    print(f"Classes: {', '.join(CLASS_NAMES)}")

    for src_split, dst_split in SPLIT_MAP.items():
        print(f"\nConverting split '{src_split}' -> '{dst_split}'...")
        n = _convert_split(raw_dataset_dir, output_dir, src_split, dst_split)
        print(f"  Wrote {n} image/label pairs into images/{dst_split} and labels/{dst_split}")

    yaml_path = _write_data_yaml(output_dir)
    print(f"\nWrote dataset config: {yaml_path}")
    print("Done.")


def main() -> None:
    """CLI entry point for dataset conversion."""
    parser = argparse.ArgumentParser(
        description="Convert NEU-DET VOC annotations to YOLO format."
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=RAW_DATASET_DIR,
        help=f"Path to raw NEU-DET dataset (default: {RAW_DATASET_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Path to YOLO output directory (default: {OUTPUT_DIR})",
    )
    args = parser.parse_args()
    convert_dataset(args.raw_dir, args.output_dir)


if __name__ == "__main__":
    main()
