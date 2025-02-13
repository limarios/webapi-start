from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from app.core.response import error_response

logger = logging.getLogger(__name__)

class GlobalErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content=error_response(message=exc.detail),
            )
        except Exception as exc:
            logger.error(f"Erro inesperado: {str(exc)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content=error_response(message="Erro interno do servidor"),
            )
