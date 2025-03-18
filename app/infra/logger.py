import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import sys

# Criar pasta de logs se não existir
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Nome do arquivo de log base (será rotacionado automaticamente)
LOG_FILE = os.path.join(LOG_DIR, "api.log")  # Nome fixo do log atual

# Configuração do handler de arquivo com rotação diária
file_handler = TimedRotatingFileHandler(
    LOG_FILE,         # Arquivo base, os backups terão sufixos
    when="midnight",  # Rotaciona à meia-noite
    interval=1,       # Intervalo de 1 dia
    backupCount=7,    # Mantém os últimos 7 dias de logs
    encoding="utf-8"  # Evita problemas com caracteres especiais
)

# Define o formato do nome dos arquivos de backup (ex: "api_2025-03-18.log")
file_handler.suffix = "%Y-%m-%d.log"

# Define a função que renomeia os arquivos rotacionados corretamente
file_handler.namer = lambda name: name.replace(".log", "")  # Remove .log duplicado

# Criar um handler para exibir logs no console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Definir encoding UTF-8 no logger
console_handler.stream = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# Formato das mensagens de log
log_format = "%(asctime)s - [%(levelname)s] - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(log_format, datefmt=date_format)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,  # Definir nível mínimo de log
    format=log_format,
    handlers=[
        file_handler,   # Salva logs no arquivo
        console_handler  # Exibe logs no console
    ]
)

# Criar logger
logger = logging.getLogger("api_logger")
logger.info("✅ Sistema de logging da API configurado com rotação diária!")
