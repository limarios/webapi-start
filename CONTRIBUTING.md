# Contribuindo com o WebAPI Start

Obrigado pelo interesse em colaborar! Este documento descreve o fluxo recomendado.

## Fluxo geral

1. **Abra uma issue** descrevendo o problema/feature antes de codar.
2. **Fork** o repositório e crie uma branch a partir de `main`:
   ```bash
   git checkout -b feat/<nome-curto-da-feature>
   ```
3. **Faça commits pequenos** seguindo o padrão de [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/).
4. **Rode o `make check`** antes de abrir o PR — ele executa lint, types e testes.
5. **Abra o Pull Request** apontando para `main`, preenchendo o template.
6. Aguarde a revisão. Pelo menos um aprove + CI verde para mergear.

## Padrão de branches

| Tipo            | Prefixo     | Exemplo                     |
|-----------------|-------------|------------------------------|
| Feature         | `feat/`     | `feat/add-refresh-token`     |
| Bugfix          | `fix/`      | `fix/jwt-expiration`         |
| Refactor        | `refactor/` | `refactor/user-repository`   |
| Documentação    | `docs/`     | `docs/update-readme`         |
| Infra / CI      | `chore/`    | `chore/upgrade-fastapi`      |

## Padrão de commits (Conventional Commits)

```
<tipo>(<escopo opcional>): <descrição curta no imperativo>

[corpo opcional explicando o porquê]

[footer opcional: BREAKING CHANGE, refs #123, etc.]
```

Tipos aceitos: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.

Exemplos:

- `feat(auth): adiciona endpoint de refresh token`
- `fix(users): corrige rota /users/me que retornava 500`
- `chore(deps): atualiza FastAPI para 0.115.7`

## Estilo de código

- Python 3.11+, type hints sempre que possível.
- Indentação: 4 espaços (configurado no `.editorconfig`).
- Limite de linha: 100 caracteres.
- Lint: `ruff` (`make lint`).
- Formatação: `black` + `ruff format` (`make format`).
- Tipos: `mypy` (`make typecheck`).

## Testes

Toda mudança de comportamento precisa de teste correspondente. Padrões aceitos:

- `tests/test_<modulo>.py` para testes funcionais via `httpx.AsyncClient`.
- `tests/test_domain_*.py` para regras de domínio puras (sem DB / sem FastAPI).

Roda toda a suíte com:

```bash
make test
```

## Code of Conduct

Este projeto adota o [Contributor Covenant](./CODE_OF_CONDUCT.md). Participar implica em
concordar com ele.
