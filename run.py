import sys
from pathlib import Path

# Adiciona o diretório 'src' ao path para poder importar os módulos corretamente
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from app.main import main

# Retorna o diretório base do projeto, estando congelado ou não
def obter_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent

if __name__ == "__main__":
    base_dir = obter_base_dir()
    main(base_dir)
