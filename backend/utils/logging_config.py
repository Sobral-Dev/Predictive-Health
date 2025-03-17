import logging
import os
from flask import request

# Criar diretório logs/ se não existir
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configuração do logger
log_file = "logs/log.txt"
logging.basicConfig(
    level=logging.INFO,  # Registra INFO, WARNINGS e ERRORS
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"), 
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Middleware para logar requisições e respostas
def log_request_response(app):
    @app.before_request
    def log_request():
        logger.info(f"📥 Requisição: {request.method} {request.path}")

    @app.after_request
    def log_response(response):
        logger.info(f"📤 Resposta: {response.status} - {response.content_type}")
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"❌ Exceção: {str(e)}", exc_info=True)

    return app
