import logging
import os
from datetime import datetime
import sys

# Criar pasta de logs se não existir
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Nome do arquivo de log baseado na data
LOG_FILE = os.path.join(LOG_DIR, f"api_{datetime.now().strftime('%Y-%m-%d')}.log")

# Criar um handler que escreve no console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Definir encoding UTF-8 no logger
console_handler.stream = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,  # Definir nível mínimo de log
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Salva logs no arquivo
        logging.StreamHandler()  # Exibe logs no console
    ]
)

# Criar logger
logger = logging.getLogger("api_logger")
