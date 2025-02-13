from fastapi import APIRouter

# Importação dos routers das features
from app.domain.auth.routes import router as auth_router
from app.infra.health import router as health_router
from app.domain.user.routes import router as user_router
from app.domain.customer.routes import router as customer_router
from app.domain.activity.routes import router as activity_router

# Criando o APIRouter principal
router = APIRouter()

# 🔥 Ajustando os prefixos corretamente
router.include_router(auth_router, prefix="/auth", tags=["Autenticação"])
router.include_router(health_router, prefix="/infra", tags=["Infraestrutura"])
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(customer_router, prefix="/customers", tags=["Customers"])
router.include_router(activity_router, prefix="/activities", tags=["Activities"])

