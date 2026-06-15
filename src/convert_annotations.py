"""Convert NEU-DET VOC annotations into YOLO format."""

from pathlib import Path


RAW_DATASET_DIR = Path("data/NEU-DET")
OUTPUT_DIR = Path("data/yolo")


def convert_dataset(raw_dataset_dir: Path = RAW_DATASET_DIR, output_dir: Path = OUTPUT_DIR) -> None:
    """Convert XML annotations and images into a YOLO-friendly layout."""
    raise NotImplementedError("Annotation conversion is not implemented yet.")


def main() -> None:
    """CLI entry point for dataset conversion."""
    convert_dataset()


if __name__ == "__main__":
    main()
