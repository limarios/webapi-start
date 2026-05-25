<div align="center">

# 🚀 WebAPI Start

**Template profissional de API em FastAPI** — Clean Architecture, DDD, PostgreSQL, JWT, Docker, CI/CD e deploy multi-cloud.

[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](.github/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

---

## 📌 Sobre

**WebAPI Start** é um *starter kit* opinativo para subir APIs Python profissionais com
o mínimo de fricção. Pensado para ser **clonado, parametrizado e evoluído** em projetos
reais — não é boilerplate de tutorial.

### Por que esse template?

- ⚙️ **Clean Architecture + DDD** de verdade — camadas separadas com dependências invertidas, não só "pastas com nomes bonitos".
- 🔐 **Segurança em primeiro lugar** — Argon2id, JWT, CORS restrito, secure headers OWASP, rate limit, scanners no CI.
- 🐳 **Docker-first** — multi-stage build, usuário não-root, healthcheck nativo, Postgres pronto via compose.
- 🧪 **Testável** — suíte com `httpx.AsyncClient` + SQLite em memória, sem precisar de Docker para rodar `pytest`.
- 🚢 **Deploy templates** prontos para **Google Cloud Run**, **AWS ECS Fargate** e **Vercel** — escolha e ative.
- 📋 **Governança completa** — `CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`, templates de issue/PR, Dependabot.

---

## 📖 Índice

1. [Stack](#-stack)
2. [Quick start](#-quick-start)
3. [Estrutura do projeto](#-estrutura-do-projeto)
4. [Variáveis de ambiente](#-variáveis-de-ambiente)
5. [Endpoints](#-endpoints)
6. [Comandos do Makefile](#-comandos-do-makefile)
7. [Testes & qualidade](#-testes--qualidade)
8. [Segurança](#-segurança)
9. [Deploy](#-deploy)
10. [Versionamento](#-versionamento)
11. [Licença](#-licença)
12. [Autor](#-autor)

---

## 🚀 Stack

| Categoria      | Tecnologia                                                              |
|----------------|--------------------------------------------------------------------------|
| Linguagem      | Python 3.11+                                                             |
| Web            | FastAPI 0.115 · Uvicorn                                                  |
| Banco          | PostgreSQL 16 · SQLAlchemy 2 (async) · asyncpg                           |
| Migrations     | Alembic                                                                  |
| Configuração   | Pydantic Settings · `.env`                                               |
| Segurança      | PyJWT 2.10 · passlib (Argon2id) · SlowAPI (rate limit)                   |
| Qualidade      | Ruff · Black · mypy · pre-commit · pytest · httpx                        |
| Containers     | Docker (multi-stage) · Docker Compose                                    |
| CI/CD          | GitHub Actions (CI + 3 templates de deploy)                              |
| Observabilidade| Logs estruturados (JSON opcional) · X-Request-ID                         |

---

## ⚡ Quick start

> **Pré-requisitos:** Docker + Docker Compose, Python 3.11+, `make`.

```bash
# 1. Clone
git clone https://github.com/limarios/webapi-start.git
cd webapi-start

# 2. Configure o ambiente
cp .env.example .env
# (opcional) gere uma SECRET_KEY forte:
python -c "import secrets; print(secrets.token_urlsafe(64))"
# ...e cole o resultado em SECRET_KEY no .env

# 3. Suba o Postgres
docker compose up -d postgres

# 4. Instale dependências (cria .venv automaticamente)
make install

# 5. Aplique as migrations
make migrate

# 6. Crie o superusuário inicial (admin@example.com / Admin@123)
make seed

# 7. Suba a API com hot-reload
make dev
```

API rodando em **http://localhost:8000**.

| Recurso         | URL                                  |
|------------------|--------------------------------------|
| Documentação    | http://localhost:8000/docs           |
| ReDoc           | http://localhost:8000/redoc          |
| Health check    | http://localhost:8000/api/v1/health  |
| OpenAPI JSON    | http://localhost:8000/openapi.json   |

> 🐳 **Tudo dentro do Docker?** Use `make docker-up` — sobe Postgres + API juntos.

---

## 🏛️ Estrutura do projeto

```text
.
├── app/
│   ├── api/                    # Camada de Apresentação (FastAPI)
│   │   ├── v1/
│   │   │   ├── routers/        # endpoints HTTP
│   │   │   ├── schemas/        # DTOs Pydantic (request/response)
│   │   │   ├── dependencies.py # DI: sessão, current_user, RBAC
│   │   │   └── router.py       # agregador
│   │   ├── error_handlers.py   # handlers globais de exceção
│   │   └── middleware.py       # secure headers, request-id
│   ├── core/                   # Cross-cutting (independente de framework)
│   │   ├── config.py           # Pydantic Settings
│   │   ├── exceptions.py       # exceções base da app
│   │   ├── logging.py          # configuração de logs (texto/JSON)
│   │   └── security.py         # JWT + hashing de senha
│   ├── domain/                 # Camada de Domínio (regras de negócio puras)
│   │   └── user/
│   │       ├── entities.py     # entidade User (dataclass)
│   │       ├── exceptions.py   # exceções do domínio
│   │       ├── repository.py   # Protocol (interface)
│   │       └── services.py     # casos de uso
│   ├── infrastructure/         # Camada de Infraestrutura (adapters)
│   │   └── database/
│   │       ├── base.py         # SQLAlchemy Base + mixins
│   │       ├── session.py      # engine async + sessão
│   │       ├── models/         # models ORM
│   │       └── repositories/   # implementações dos repositórios
│   ├── bootstrap.py            # cria superusuário inicial
│   └── main.py                 # application factory
├── alembic/                    # migrations
├── tests/                      # suíte de testes
├── deploy/                     # templates de deploy (AWS, GCP, Vercel)
├── .github/                    # workflows, templates, dependabot
├── docker-compose.yml          # Postgres + API
├── Dockerfile                  # multi-stage, non-root
├── pyproject.toml              # Ruff, Black, mypy, pytest, coverage
├── requirements.txt            # deps de runtime
├── requirements-dev.txt        # deps de dev
└── Makefile                    # atalhos de DX
```

### Camadas (Dependency Rule)

```
       ┌─────────────────────────────────────────┐
       │  api/  (FastAPI routers, Pydantic DTOs) │
       └─────────────┬───────────────────────────┘
                     │ depende de
       ┌─────────────▼───────────────────────────┐
       │  domain/  (entities, services, ports)   │
       └─────────────┬───────────────────────────┘
                     │ é implementado por
       ┌─────────────▼───────────────────────────┐
       │  infrastructure/  (SQLAlchemy adapters) │
       └─────────────────────────────────────────┘

  core/ é transversal (config, security, logging) e não importa
  nada das outras camadas — pode ser usado por todas.
```

A regra é simples: **o domínio não conhece SQLAlchemy nem FastAPI**.
A `infrastructure` implementa os contratos do domínio. A `api` orquestra
chamando os serviços do domínio com seus adapters injetados.

---

## 🔧 Variáveis de ambiente

Veja [`.env.example`](.env.example) — está documentado linha a linha.
Principais:

| Variável                       | Default                   | Função                                              |
|--------------------------------|---------------------------|-----------------------------------------------------|
| `APP_ENV`                      | `development`             | `development` \| `testing` \| `production`           |
| `APP_DEBUG`                    | `false`                   | Liga modo debug                                     |
| `POSTGRES_HOST`                | `localhost`               | Use `postgres` se a API roda dentro do compose       |
| `POSTGRES_USER`                | `admin`                   | Usuário do Postgres                                 |
| `POSTGRES_PASSWORD`            | `admin`                   | Senha do Postgres (**troque em produção**)          |
| `POSTGRES_DB`                  | `webapi_start`            | Nome do database                                    |
| `SECRET_KEY`                   | —                         | **Obrigatório.** Gere com `secrets.token_urlsafe`   |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | `15`                      | Validade do JWT (curto por design)                  |
| `CORS_ORIGINS`                 | `http://localhost:3000`   | Origens permitidas (CSV) · `*` proibido em prod     |
| `RATE_LIMIT_PER_MINUTE`        | `60`                      | Requests/minuto por IP (global)                     |
| `LOGIN_RATE_LIMIT_PER_MINUTE`  | `5`                       | Tentativas de login/minuto por IP                    |
| `LOG_LEVEL`                    | `INFO`                    | Nível mínimo de logs                                |
| `LOG_JSON`                     | `false`                   | `true` em produção para logs estruturados           |
| `FIRST_SUPERUSER_EMAIL`        | `admin@example.com`       | Usuário admin criado pelo `make seed`               |
| `FIRST_SUPERUSER_PASSWORD`     | `Admin@Pass123!`          | Senha do admin (**bloqueada em produção se default**) |

---

## 📡 Endpoints

Todos versionados sob `/api/v1`. Endpoints protegidos exigem `Authorization: Bearer <jwt>`.

### Health

| Método | Rota                 | Descrição                          |
|--------|----------------------|-------------------------------------|
| GET    | `/api/v1/health`     | Status geral + check do banco       |
| GET    | `/api/v1/health/live`| Liveness probe (k8s)                |
| GET    | `/api/v1/health/ready`| Readiness probe (k8s)              |

### Autenticação

| Método | Rota                  | Descrição                                       |
|--------|------------------------|-------------------------------------------------|
| POST   | `/api/v1/auth/login`  | Login (form data `username` = email, `password`) |

### Usuários

| Método | Rota                       | Auth   | Descrição                  |
|--------|----------------------------|--------|----------------------------|
| GET    | `/api/v1/users/me`         | user   | Dados do usuário atual     |
| POST   | `/api/v1/users/`           | admin  | Cria um usuário            |
| GET    | `/api/v1/users/`           | admin  | Lista usuários (paginado)  |
| GET    | `/api/v1/users/{user_id}`  | admin  | Detalha usuário            |
| PATCH  | `/api/v1/users/{user_id}`  | admin  | Atualiza usuário           |
| DELETE | `/api/v1/users/{user_id}`  | admin  | Remove usuário             |

Schema de erro padronizado:

```json
{
  "code": "user_not_found",
  "message": "Usuário não encontrado",
  "details": null
}
```

---

## 🛠️ Comandos do Makefile

```text
make help          Mostra essa ajuda
make install       Cria venv e instala dependências (dev)
make dev           Sobe a API com hot-reload
make run           Sobe a API em modo produção (sem reload)
make test          Roda a suíte de testes com cobertura
make lint          Lint com Ruff
make format        Formata com Ruff + Black
make typecheck     Verifica tipos com mypy
make check         lint + typecheck + testes (CI local)
make db-up         Sobe somente o Postgres
make db-down       Para o Postgres
make db-logs       Logs do Postgres
make migrate       Aplica migrations
make migration m="msg"   Gera nova migration autogerada
make seed          Cria o superusuário inicial
make docker-build  Build da imagem da API
make docker-up     Sobe stack completa (Postgres + API)
make docker-down   Derruba a stack completa
make clean         Limpa caches e artefatos
```

---

## 🧪 Testes & qualidade

```bash
make check     # lint + types + testes (o que o CI roda)
make test      # só testes com cobertura
```

A suíte roda contra **SQLite em memória** via `aiosqlite` — não precisa de Docker
local para `pytest`. Cobertura mínima configurada em **70%** no `pyproject.toml`.

Hooks de pre-commit:

```bash
pre-commit install
pre-commit run --all-files
```

---

## 🔐 Segurança

| Controle                          | Status |
|------------------------------------|:------:|
| Hashing de senha com Argon2id      | ✅     |
| Defesa contra user enumeration (timing-safe) | ✅ |
| JWT assinado HS256 + algoritmo travado por `Literal` | ✅ |
| JWT sem PII (apenas `sub` + `role`) | ✅     |
| Senhas com complexidade mínima (12+ chars, blacklist) | ✅ |
| Schemas separados admin/self (anti mass-assignment) | ✅ |
| Headers OWASP completos (HSTS, CSP, COOP, CORP, X-Frame…) | ✅ |
| CORS restrito (rejeita `*` + exige HTTPS em prod) | ✅ |
| Rate limit global + rate limit dedicado no login | ✅ |
| RBAC (role `admin`)                | ✅     |
| `sslmode=require` automático em prod | ✅     |
| Bootstrap recusa senha default em prod | ✅ |
| Imagem Docker não-root             | ✅     |
| `bandit` SAST no CI                | ✅     |
| `pip-audit` bloqueante no CI       | ✅     |
| `gitleaks` para secrets no pre-commit/CI | ✅ |
| Validação rigorosa via Pydantic    | ✅     |
| Erros consistentes sem vazar stack | ✅     |

Veja [SECURITY.md](SECURITY.md) para reportar vulnerabilidades.

---

## 🚢 Deploy

Templates prontos em [`deploy/`](deploy/README.md):

| Provedor          | Indicado para                                | Workflow                                 |
|-------------------|----------------------------------------------|-------------------------------------------|
| Google Cloud Run  | Scale-to-zero, MVPs, custo baixo             | [.github/workflows/deploy-cloud-run.yml](.github/workflows/deploy-cloud-run.yml) |
| AWS ECS Fargate   | Empresas já na AWS, VPC privada, ALB         | [.github/workflows/deploy-aws-ecs.yml](.github/workflows/deploy-aws-ecs.yml) |
| Vercel            | Demos rápidas (limitações descritas)         | [.github/workflows/deploy-vercel.yml](.github/workflows/deploy-vercel.yml) |

Cada workflow vem com `if: false` por padrão para evitar deploy acidental.
Siga o README do diretório `deploy/<provedor>/` para configurar e ativar.

---

## 🏷️ Versionamento

Este projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

- `MAJOR.MINOR.PATCH`
- Releases automáticas via tag `vX.Y.Z` (workflow `.github/workflows/release.yml`).
- Mudanças notáveis em [CHANGELOG.md](CHANGELOG.md).

Versão atual: **v1.1.0** — release de hardening de segurança (CVE patch + OWASP).

---

## 📜 Licença

[MIT](LICENSE) © 2026 LimaRios.dev

---

## 👤 Autor

**Matheus de Lima Rios**

- ✉️ contato@limarios.dev
- 🌐 [limarios.dev](https://limarios.dev)
- 💼 [LinkedIn](https://www.linkedin.com/in/limarios/)

> Este projeto é open source e serve como base para acelerar a construção de APIs Python
> profissionais. Sinta-se à vontade para usar, adaptar e contribuir.
