import json
from dotenv import dotenv_values

# Carrega .env
def load_env(name, BASE_DIR, env_subdir='envs'):
    path = BASE_DIR / 'resources' / env_subdir / f"{name}.env"
    if not path.exists():
        raise FileNotFoundError(f"Arquivo .env '{name}' não encontrado em {path}")
    return dotenv_values(path)

# Carrega .json
def load_json(name, BASE_DIR, json_subdir='selectors'):
    path = BASE_DIR / 'resources' / json_subdir / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Arquivo JSON '{name}' não encontrado em {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
