# Política de Segurança

## Versões suportadas

| Versão | Suportada |
|--------|-----------|
| 1.x    | ✅        |
| < 1.0  | ❌        |

## Reportando uma vulnerabilidade

Se você encontrou uma vulnerabilidade de segurança neste projeto, **não abra uma
issue pública**. Em vez disso:

1. Envie um e-mail para **limariosprofissional@gmail.com** com o assunto
   `[SECURITY] webapi-start - <título curto>`.
2. Inclua:
   - Descrição da vulnerabilidade
   - Passo a passo de reprodução (PoC se possível)
   - Impacto estimado
   - Versão afetada e ambiente
3. Aguarde retorno em até **5 dias úteis**.

## Compromisso

- Confirmaremos o recebimento em 48h úteis.
- Forneceremos uma estimativa inicial em até 5 dias úteis.
- Trabalharemos com você na correção e na divulgação coordenada.
- Daremos crédito (se desejado) no `CHANGELOG.md` e nas release notes.

## Boas práticas adotadas pelo projeto

- Hashing de senha com **Argon2id** (fallback bcrypt para legado).
- JWT assinado com `HS256` (suporte a trocar para `RS256` em ambientes maiores).
- Cabeçalhos HTTP de segurança (HSTS, X-Content-Type-Options, etc.) habilitados.
- CORS restrito por lista de origens.
- Rate limiting por IP (configurável).
- Dependências auditadas via `pip-audit` e SAST via `bandit` no CI.
- Detecção de segredos vazados via `gitleaks` no pre-commit e no CI.
- Imagem Docker rodando como usuário **não-root**.
- Variáveis sensíveis carregadas exclusivamente do ambiente / Secret Manager.
