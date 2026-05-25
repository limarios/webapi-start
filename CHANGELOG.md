# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este
projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Planejado

- Refresh token endpoint com rotation + reuse detection
- Denylist de JWT via Redis (revogação imediata)
- 2FA TOTP (RFC 6238)
- Account lockout incremental (backoff por user_id)
- Recovery de senha por e-mail
- Observabilidade: OpenTelemetry + traces exportados para OTLP

## [1.1.0] — 2025-01-02

Release de hardening de segurança baseada em auditoria pré-deploy.
**Sem breaking changes funcionais**, mas senhas precisam atender ao novo
requisito de complexidade (12+ chars). Atualize `FIRST_SUPERUSER_PASSWORD`
se estiver usando o default.

### Corrigido — CRITICAL

- **JWT**: migrado de `python-jose==3.3.0` (CVE-2024-33663/33664) para `PyJWT==2.10.1` (sem CVE conhecida, manutenção ativa).
- **JWT**: `JWT_ALGORITHM` agora é `Literal[...]` validado em runtime — bloqueia *algorithm confusion* operacional.
- **JWT**: `decode_token` exige claims `exp`, `iat`, `sub` obrigatórias.
- **Auth**: defesa contra *user enumeration por timing* — verify dummy de Argon2 quando o usuário não existe.
- **Schemas**: separação `AdminUserUpdate` (com `role`/`is_active`) vs `SelfUserUpdate` (sem campos privilegiados) — fecha *mass assignment* latente.
- **JWT**: TTL default reduzido de 30 para 15 minutos; documentação completa sobre ausência de denylist em `SECURITY.md`.

### Corrigido — MAJOR

- **Rate limit**: `/auth/login` ganha limite dedicado (default 5/min/IP); `X-Forwarded-For` é resolvido como IP real atrás de proxy.
- **JWT**: removido `email` dos claims — apenas `sub` (UUID) e `role` viajam no token. PII fica em `/users/me`.
- **Headers**: adicionados `Content-Security-Policy`, `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`.
- **Bootstrap**: recusa rodar em produção quando `FIRST_SUPERUSER_PASSWORD` está com o valor default.
- **Settings**: `model_validator` recusa boot em produção quando `CORS_ORIGINS` contém `*` ou origem não-HTTPS.
- **Settings**: `SECRET_KEY` com valor de exemplo (contendo "change-me" ou "test") é rejeitada em produção.
- **DB**: produção exige `ssl=require` (auto-injetado em `DATABASE_URL` quando ausente).
- **Senha**: validação rigorosa via Pydantic `AfterValidator` — 12+ chars, upper+lower+dígito+símbolo, blacklist de senhas comuns.
- **CI**: `pip-audit` agora é bloqueante (removido `continue-on-error: true`); `SECRET_KEY` do CI é gerada em runtime via `openssl rand -hex 48`.

### Adicionado

- `app/core/rate_limit.py` — instância central do SlowAPI com `X-Forwarded-For` awareness.
- `app/core/security.py::consume_dummy_verify()` — utilitário para defesa de timing.
- `StrongPassword` annotated type em `app/api/v1/schemas/user.py`.
- `permissions: contents: read` explícito no `ci.yml` (princípio do menor privilégio).
- Seção "Limitações conhecidas (roadmap)" em `SECURITY.md` documentando ausência de denylist, lockout incremental e 2FA — com critérios para ligar cada uma.

### Mudado

- Versão `app.APP_VERSION` e `pyproject.toml` bumpadas para 1.1.0.
- `tests/conftest.py` e `tests/test_*.py` atualizados com senhas que respeitam a nova regra de complexidade.

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

[Não lançado]: https://github.com/limarios/webapi-start/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/limarios/webapi-start/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/limarios/webapi-start/releases/tag/v1.0.0
