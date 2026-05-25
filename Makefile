# =============================================================================
# WebAPI Start - Makefile
# Atalhos para DX. Em Windows, use Git Bash, WSL ou substitua pelo comando direto.
# =============================================================================

.PHONY: help install dev test lint format typecheck check db-up db-down db-logs \
        migrate migration seed run docker-build docker-up docker-down clean

PYTHON ?= python
VENV   ?= .venv
PIP    := $(VENV)/bin/pip
PY     := $(VENV)/bin/python

ifeq ($(OS),Windows_NT)
	PIP := $(VENV)/Scripts/pip
	PY  := $(VENV)/Scripts/python
endif

help:  ## Mostra essa ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install:  ## Cria venv e instala dependências (dev)
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt
	$(PY) -m pre_commit install

dev:  ## Sobe a API com hot-reload (precisa de .env e do Postgres rodando)
	$(PY) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run:  ## Sobe a API em modo produção (sem reload)
	$(PY) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

test:  ## Roda a suíte de testes com cobertura
	$(PY) -m pytest --cov=app --cov-report=term-missing --cov-report=xml

lint:  ## Lint com Ruff
	$(PY) -m ruff check app tests

format:  ## Formata com Ruff + Black
	$(PY) -m ruff check --fix app tests
	$(PY) -m black app tests

typecheck:  ## Verifica tipos com mypy
	$(PY) -m mypy app

check: lint typecheck test  ## Roda lint + typecheck + testes (CI local)

db-up:  ## Sobe somente o Postgres
	docker compose up -d postgres

db-down:  ## Para o Postgres
	docker compose stop postgres

db-logs:  ## Logs do Postgres
	docker compose logs -f postgres

migrate:  ## Aplica migrations
	$(PY) -m alembic upgrade head

migration:  ## Gera uma nova migration autogerada (ex: make migration m="add users")
	$(PY) -m alembic revision --autogenerate -m "$(m)"

seed:  ## Cria o superusuário inicial usando o .env
	$(PY) -m app.bootstrap

docker-build:  ## Build da imagem da API
	docker compose --profile full build

docker-up:  ## Sobe stack completa (Postgres + API)
	docker compose --profile full up -d

docker-down:  ## Derruba a stack completa
	docker compose --profile full down

clean:  ## Limpa caches e artefatos
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml htmlcov build dist *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
