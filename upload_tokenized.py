import kaggle
import json
from pathlib import Path

tmp = Path("/tmp/tokenized_cache")
username = kaggle.api.get_config_value(kaggle.api.CONFIG_NAME_USER)
print(f"User: {username}")

# Create a temp directory for the upload
import shutil
import tempfile
upload_dir = Path(tempfile.mkdtemp())

# Copy tokenized data
shutil.copytree(tmp, upload_dir / "tokenized")

# Create metadata
meta = {
    "id": f"{username}/byt5-tokenized-400k",
    "title": "ByT5 OCR Tokenized 400k",
    "licenses": [{"name": "CC0-1.0"}],
    "description": "Tokenized dataset of 400k OCR calibration pairs for ByT5 fine-tuning. Each sample has input_ids, attention_mask, and labels for the noisy→clean medical text correction task.",
    "keywords": ["byt5", "ocr", "medical", "tokenized", "calibration"],
    "categories": ["Computer Vision", "Natural Language Processing"],
}

with open(upload_dir / "dataset-metadata.json", "w") as f:
    json.dump(meta, f)

print(f"Creating dataset from {upload_dir}...")
kaggle.api.dataset_create_new(str(upload_dir), public=True, quiet=False, convert_to_csv=False, dir_mode="zip")
print("Done!")