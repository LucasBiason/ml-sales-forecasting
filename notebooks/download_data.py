import kagglehub
import shutil
from pathlib import Path

# Download latest version
path = kagglehub.dataset_download("lorentzyeung/price-paid-data-202304")
print("Path to dataset files:", path)

# Copiar para nossa pasta data/
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Copiar arquivos baixados
source = Path(path)
for file in source.glob("*"):
    if file.is_file():
        shutil.copy(file, data_dir / file.name)
        print(f"Copiado: {file.name}")

print("\nDados salvos em:", data_dir.absolute())
