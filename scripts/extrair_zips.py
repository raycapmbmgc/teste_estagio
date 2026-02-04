import zipfile
from pathlib import Path

ZIP_DIR = Path("data/raw")
EXTRACT_DIR = Path("data/extracted")

EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

for zip_file in ZIP_DIR.glob("*.zip"):
    print(f"Extraindo {zip_file.name}")

    with zipfile.ZipFile(zip_file, "r") as z:
        # cria pasta com nome do zip (1T2025, 2T2025...)
        pasta_destino = EXTRACT_DIR / zip_file.stem
        pasta_destino.mkdir(exist_ok=True)

        z.extractall(pasta_destino)

print("✔ Extração finalizada")
