# logger.py
import logging
from datetime import datetime
import os

def log_config(base_path):
    # Garante que a pasta de logs existe
    log_dir = os.path.join(base_path, "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Cria o nome do arquivo de log com data/hora
    log_filename = datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.txt")
    full_log_path = os.path.join(log_dir, log_filename)

    # Configuração do logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(full_log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    # Exporta o caminho do arquivo para uso externo
    return full_log_path
