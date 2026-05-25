# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este
projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Planejado

- Refresh token endpoint
- Recovery de senha por e-mail
- Domínio de exemplo adicional (Items) para demonstrar agregados relacionados
- Observabilidade: OpenTelemetry + traces exportados para OTLP

## [1.0.0] — 2025-01-01

### Adicionado

- Estrutura base em **Clean Architecture + Domain-Driven Design**:
  `app/{api,core,domain,infrastructure}`.
- Domínio `User` com entidade pura, repositório como Protocol e implementação
  SQLAlchemy assíncrona.
- Autenticação **OAuth2 password flow + JWT** (`/api/v1/auth/login`).
- CRUD de usuários protegido por **RBAC** (role `admin`).
- Endpoints de saúde: `/api/v1/health`, `/health/live`, `/health/ready`.
- Hashing de senha com **Argon2id**.
- **Cabeçalhos de segurança** OWASP via middleware.
- **CORS** configurável por variável de ambiente.
- **Rate limit** por IP (SlowAPI).
- Tratamento global de exceções com payload de erro consistente
  (`{code, message, details}`).
- Configuração via **Pydantic Settings** + `.env`.
- Logging configurável em texto ou **JSON** (production-ready).
- **Docker multi-stage** com usuário não-root e healthcheck.
- **docker-compose** com Postgres 16 + healthcheck nativo.
- **Alembic** configurado e primeira migration `users`.
- Bootstrap do superusuário inicial (`python -m app.bootstrap`).
- **Makefile** com atalhos de DX (`install`, `dev`, `test`, `migrate`, ...).
- Suíte de testes em **pytest + httpx AsyncClient** rodando contra SQLite em memória.
- **CI** completo no GitHub Actions: lint, format, types, testes com cobertura,
  Bandit, pip-audit, Gitleaks, build Docker.
- **Templates de deploy** para Google Cloud Run, AWS ECS Fargate e Vercel
  (workflows desabilitados por padrão até o usuário configurar secrets).
- Documentação de governança: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY,
  templates de issue e pull request.

[Não lançado]: https://github.com/limarios/webapi-start/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/limarios/webapi-start/releases/tag/v1.0.0
