# Model Weights

Trained YOLO11 weights are **not stored in this repository** (they are large binary files). After fine-tuning on the NEU-DET dataset, the best checkpoint is published on Hugging Face for reuse.

## Download

Replace `YOUR_USERNAME` with your Hugging Face account (e.g. `aimanahmed495-max`) once training is complete.

### Option 1 — Hugging Face CLI (recommended)

```bash
pip install huggingface_hub
huggingface-cli download YOUR_USERNAME/steel-defect-yolo11 best.pt --local-dir models
```

### Option 2 — Python

```python
from huggingface_hub import hf_hub_download

path = hf_hub_download(
    repo_id="YOUR_USERNAME/steel-defect-yolo11",
    filename="best.pt",
    local_dir="models",
)
print(f"Saved to {path}")
```

### Option 3 — Manual download

1. Open [huggingface.co/YOUR_USERNAME/steel-defect-yolo11](https://huggingface.co/YOUR_USERNAME/steel-defect-yolo11)
2. Download `best.pt`
3. Place it at `models/best.pt`

## Verify

The API reads the path from `MODEL_PATH` in `.env` (default: `models/best.pt`). After downloading:

```bash
ls models/best.pt
```

## Training your own

See `notebooks/train_colab.ipynb` for the full fine-tuning workflow, or run locally:

```bash
python -m src.convert_annotations
python -m src.train
```

Weights are written to `runs/detect/train/weights/best.pt` by Ultralytics. Copy or upload that file to Hugging Face and update the repo ID above.
