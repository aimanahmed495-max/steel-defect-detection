# steel-defect-detection

Computer vision pipeline for steel surface defect detection. A fine-tuned YOLO11 model detects defects, OpenCV handles preprocessing and visualization, and a vision-language model generates a natural-language quality report.

## Status

This repository is currently scaffolded for development. The folder structure and starter files are in place so the NEU-DET dataset can be added next.

## Planned Structure

```text
steel-defect-detection/
├── data/
│   └── .gitkeep
├── models/
│   └── .gitkeep
├── src/
│   ├── convert_annotations.py
│   ├── train.py
│   ├── pipeline.py
│   └── vlm.py
├── api/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .env
├── .gitignore
├── .cursorrules
├── requirements.txt
└── README.md
```

## Dataset Placement

Download the NEU-DET dataset from Kaggle and place it under `data/` after setup. The conversion script will expect the raw dataset to live in a path like `data/NEU-DET/`.

## Next Build Steps

1. Add the NEU-DET dataset under `data/NEU-DET/`.
2. Implement `src/convert_annotations.py` to convert VOC XML annotations into YOLO format.
3. Implement `src/train.py` to fine-tune YOLO11 on the converted dataset.
4. Implement `src/pipeline.py` for CLAHE preprocessing, detection, annotation, and cropping.
5. Implement `src/vlm.py` for OpenAI or Anthropic defect report generation.
6. Connect everything through `api/main.py` and the vanilla JS frontend.

## Setup

Create a virtual environment and install the starter dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Then create or update `.env` with your model and API settings.
