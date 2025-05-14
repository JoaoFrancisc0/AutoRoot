from src.common import json


# Carrega .json
def load_json(name, BASE_DIR, json_subdir):
    path = BASE_DIR / 'resources' / json_subdir / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Arquivo JSON '{name}' não encontrado em {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
