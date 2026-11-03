# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este
projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Alterado

- **Python**: mínimo passa a ser 3.12 (`requires-python`, ruff/black/mypy); `.python-version` fixa **3.13**, usado pelo CI, e a imagem Docker sobe de `python:3.11-slim` para `python:3.13-slim`.
- **CI**: todas as actions pinadas por SHA de commit (tag no comentário), `timeout-minutes` em todos os jobs; `docker/setup-buildx-action` v3→v4 e `aws-actions/configure-aws-credentials` v4→v6 (template ECS).
- **Deploy Vercel (template)**: CLI fixada em `vercel@65.10.0` em vez de `@latest`.
- **Dependabot**: pip semanal com grupos minor/patch e de segurança (majors continuam individuais), docker mensal com a linha do Python travada em 3.13, actions mensal agrupado.
- **pre-commit**: revs de ruff/black alinhadas aos pins de `requirements-dev.txt`; hook `fix-byte-order-marker`.
- **Deps** (Dependabot, desde a v1.1.0): `PyJWT` 2.13.0→2.15.0 (CVEs apontadas pelo `pip-audit --strict`), `pydantic` 2.10.6→2.13.5, `pydantic-settings` 2.7.1→2.16.2, `email-validator` 2.2.0→2.3.0, `slowapi` 0.1.9→0.1.10, `asyncpg` 0.30.0→0.31.0, `ruff` 0.9.2→0.16.7, `black` 24.10.0→26.10.1, `pytest-cov` 6.0.0→7.1.0; actions `checkout` v7, `setup-python` v7, `upload-artifact` v7, `docker/build-push-action` v7, `gitleaks-action` v3, `google-github-actions/auth` e `setup-gcloud` v3, `action-gh-release` v3.

### Removido

- Workflow `auto-merge-dependabot.yml`: sem branch protection exigindo o CI, o `gh pr merge --auto` mesclava sem gate.

### Corrigido

- **mypy** (passo informativo): com `python_version = "3.11"` ele abortava com "Found 1 error in 1 file" ao analisar `deprecated/sphinx.py`, que usa a sintaxe `type X = ...` (PEP 695, só 3.12+). Com `python_version = "3.12"` a análise volta a rodar e acusa 6 erros de tipo pré-existentes em 5 arquivos (o passo segue `continue-on-error`; limpeza em issue própria).
- `.env.example` passa a documentar `POSTGRES_SSL_REQUIRED`, lida por `app/core/config.py`.
- **Datas das versões**: 1.0.0 e 1.1.0 estavam datadas de jan/2025, mas as tags `v1.0.0` e `v1.1.0` foram criadas em 2026-05-25; as datas abaixo foram alinhadas às tags.
- **CI**: `pip-audit` e `bandit` passam a ser instalados via `requirements-dev.txt` (o job `quality` falhava com `exit 127` porque nenhum step os instalava).
- **Deps**: remediação das CVEs apontadas pelo `pip-audit --strict` — `PyJWT` 2.10.1→2.13.0, `python-multipart` 0.0.20→0.0.31 e `fastapi` 0.115.7→0.133.0 (primeira versão sem o teto `starlette<1.0`, liberando `starlette>=1.3.1`).
- **Settings**: `DATABASE_URL` aceita qualquer esquema (`AnyUrl`) — `PostgresDsn` rejeitava o `sqlite+aiosqlite` usado pela suíte de testes.
- **DB**: `pool_size`/`max_overflow` só são passados ao engine quando o dialeto não é SQLite (o `StaticPool` os rejeita).
- **Auth**: `/auth/login` recebe `response: Response`, exigido pelo SlowAPI com `headers_enabled=True` para injetar `X-RateLimit-*`.
- **Testes**: `LOGIN_RATE_LIMIT_PER_MINUTE` elevado no ambiente de teste e e-mails das fixtures trocados de `.local` (TLD reservado, recusado pelo `email-validator`) para `example.com`.

### Planejado

- Refresh token endpoint com rotation + reuse detection
- Denylist de JWT via Redis (revogação imediata)
- 2FA TOTP (RFC 6238)
- Account lockout incremental (backoff por user_id)
- Recovery de senha por e-mail
- Observabilidade: OpenTelemetry + traces exportados para OTLP

## [1.1.0] — 2026-05-25

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

## [1.0.0] — 2026-05-25

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
