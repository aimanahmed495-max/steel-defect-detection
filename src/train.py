"""Training entry point for the steel defect detector."""

from pathlib import Path


DATA_CONFIG = Path("data/yolo/data.yaml")
DEFAULT_MODEL = "yolo11n.pt"


def train_model(data_config: Path = DATA_CONFIG, base_model: str = DEFAULT_MODEL) -> None:
    """Fine-tune YOLO11 on the converted NEU-DET dataset."""
    raise NotImplementedError("Training is not implemented yet.")


def main() -> None:
    """CLI entry point for model training."""
    train_model()


if __name__ == "__main__":
    main()
