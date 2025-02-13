from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.infra.logger import logger

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """ Loga erros HTTP específicos """
    logger.error(f"Erro {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """ Loga erros inesperados """
    logger.critical(f"Erro inesperado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Erro interno no servidor"}
    )
