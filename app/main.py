from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuth2 as OAuth2Model
from fastapi import HTTPException
import uvicorn

from app.api.v1.endpoints.routes import router as api_router

from app.core.config import get_settings
from app.core.error_handler import custom_http_exception_handler, generic_exception_handler

from app.infra.logger import logger  # ✅ Importando logger corretamente
from app.infra.middleware import GlobalErrorHandlerMiddleware
from app.infra.monitoring import setup_monitoring

settings = get_settings()

# 🔥 Ajustando tokenUrl no Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
security_scheme = OAuth2Model(
    flows=OAuthFlowsModel(password={"tokenUrl": "/api/v1/auth/token"}),
)

app = FastAPI(
    title="API Start",
    description=(
        "Esta API foi desenvolvida como projeto start e serve como o núcleo central para desenvolvimento de API. "
        "Baseada em princípios modernos, como Clean Architecture e Domain-Driven Design, "
        "a API integra, gerencia e orquestra processos gerais de uma API completa. "
        "Projetada para ser flexível, robusta e escalável, ela permite a evolução contínua e a integração com sistemas legados "
        "e futuros, garantindo segurança, desempenho e manutenibilidade em suas operações."
    ),
    contact={
        "name": "Dev: Matheus de Lima Rios",
        "email": "limariosprofissional@gmail.com",
        "url": "https://agenciatechcoffee.com"
    },
    version="1.0.0",
    openapi_tags=[
        {"name": "Autenticação", "description": "Operações relacionadas à autenticação"},
        {"name": "Infraestrutura", "description": "Serviços de Infraestrutura da API"},
        {"name": "Users", "description": "Operações relacionadas aos Usuários"},
        {"name": "Customers", "description": "Operações relacionadas aos Clientes"},
        {"name": "Activities", "description": "Operações relacionadas as Atividades"},       
    ],
    openapi_components={"securitySchemes": {"OAuth2PasswordBearer": security_scheme}},
    debug=settings.DEBUG
)

# Configurar métricas Prometheus
setup_monitoring(app)

# Tratamento de exceções
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Adiciona middleware de erro global
app.add_middleware(GlobalErrorHandlerMiddleware)

# Inclui as rotas corretamente
app.include_router(api_router, prefix="/api/v1")

# Middleware para log de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Recebendo requisição: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Resposta: {response.status_code}")
    return response

@app.get("/")
def root():
    return {"message": "API está online!", "environment": settings.ENV}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
