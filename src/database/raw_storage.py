import json
from pathlib import Path


RAW_DIR = Path("data/raw")


def save_json(data, filename):
    file_path = RAW_DIR / filename

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Données sauvegardées dans : {file_path}")
    
    
def load_json(filename):
    file_path = RAW_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)