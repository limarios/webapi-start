from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text  # ✅ Importar `text` corretamente
from app.db.session import get_db
import logging

router = APIRouter()

@router.get("/health", summary="Health Check da API")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Verifica o status da API e do Banco de Dados.
    """
    try:
        # ✅ Corrigindo erro da query SQL
        result = await db.execute(text("SELECT 1"))
        db_status = "connected" if result.scalar() == 1 else "disconnected"
        return {
            "status": "ok",
            "database": db_status
        }
    except Exception as e:
        logging.error(f"❌ Erro no banco de dados: {e}")
        return {
            "status": "error",
            "database": "disconnected"
        }
