from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

folders = [
    "data/raw/handwritten_dolil",
    "data/raw/deed_samples",
    "data/raw/dlrs_forms",
    "data/synthetic",
    "data/processed",
    "notebooks",
    "src",
    "tests",
    "app",
]

for folder in folders:
    (ROOT / folder).mkdir(parents=True, exist_ok=True)

print("Project root:", ROOT)
print("Folder setup: DONE")
