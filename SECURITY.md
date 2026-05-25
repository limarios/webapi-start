# Política de Segurança

## Versões suportadas

| Versão | Suportada |
|--------|-----------|
| 1.1.x  | ✅        |
| 1.0.x  | ⚠️ apenas patches de segurança críticos |
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

### Autenticação e sessões
- Hashing de senha com **Argon2id** (parâmetros default do `argon2-cffi`, OWASP-aligned).
- **PyJWT** ≥ 2.10 (sem CVE pendente; substitui `python-jose` que estava em modo manutenção).
- `JWT_ALGORITHM` restrito por `Literal[...]` em runtime — impede *algorithm confusion*.
- Tokens carregam apenas `sub` (UUID do usuário) e `role`. **Sem PII** (email, nome) nos claims.
- Validação obrigatória das claims `exp`, `iat`, `sub` em todo `decode`.
- TTL curto por default: 15 minutos para access token.
- Defesa contra *user enumeration por timing*: senha é sempre verificada contra um hash dummy quando o usuário não existe, nivelando o tempo de resposta.

### Autorização
- RBAC por role (`admin`/`user`) aplicado nos endpoints sensíveis via `require_admin`.
- Schemas de update separados: `AdminUserUpdate` (com `role`, `is_active`) é distinto de `SelfUserUpdate` — impede *mass assignment* / privilege escalation por reuso de schema em rotas self-service.

### Configuração
- `SECRET_KEY` obrigatória, `min_length=32`, validada em runtime; valores de exemplo são rejeitados em produção.
- `Settings` recusa boot em produção quando:
  - `CORS_ORIGINS` contém `*` ou usa esquema não-HTTPS;
  - `DATABASE_URL` não exige SSL (auto-injeta `ssl=require` para asyncpg);
  - `FIRST_SUPERUSER_PASSWORD` está com valor padrão.
- Variáveis sensíveis carregadas exclusivamente do ambiente / Secret Manager.

### Rede e HTTP
- **CORS restrito** por lista de origens (`allow_credentials=True` + sem wildcard).
- Cabeçalhos de segurança (OWASP):
  - `Strict-Transport-Security: max-age=63072000; includeSubDomains`
  - `Content-Security-Policy` (frame-ancestors 'none', sem `unsafe-eval`)
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy`
  - `Cross-Origin-Opener-Policy: same-origin`
  - `Cross-Origin-Resource-Policy: same-site`
- **Rate limiting** dual:
  - Global por IP via SlowAPI (default 60/min).
  - Dedicado no `/auth/login` (default 5/min) para mitigar brute-force.
- `X-Forwarded-For` resolvido como IP real do cliente atrás de proxy.

### Senha
- Mínimo **12 caracteres**.
- Exige maiúscula + minúscula + dígito + símbolo.
- Rejeita senhas em lista de senhas comuns.
- Hash Argon2id, sem armazenamento da senha em texto.

### Banco de dados
- ORM (SQLAlchemy 2 async) elimina SQL injection em queries do projeto.
- `sslmode=require` automático em produção.
- Pool com `pool_pre_ping=True`.

### Build e CI
- Imagem Docker **multi-stage**, rodando como usuário não-root, com healthcheck.
- CI roda:
  - Ruff (lint) — `select` agressivo incluindo `S` (bandit) e `B` (bugbear)
  - Black (format check)
  - mypy (type check)
  - pytest + cobertura
  - **bandit** (SAST)
  - **pip-audit** com `--strict` — quebra build em CVE de dependência
  - **gitleaks** (secret scanning) no pre-commit e no CI
- `GITHUB_TOKEN` com `permissions` mínimas em cada workflow.

## Limitações conhecidas (roadmap)

Estas limitações são **intencionais** na v1.1.0 para manter o template enxuto, mas estão
documentadas para você decidir quando adicionar. Cada item tem complexidade adicional
significativa e não deve ser ligado sem entender o trade-off.

### Sem revogação de JWT (denylist / refresh rotation)

A v1.1.0 **não** implementa lista de revogação de tokens. Consequências:

- Um token vazado é válido até `exp` (15 min por default).
- `logout` é puramente client-side (descartar o token).
- Desativar um usuário (`is_active=false`) **invalida o token na requisição seguinte**
  porque `get_current_user` consulta o DB a cada chamada — mas o token, tecnicamente,
  continua aceito pelo `decode_token` até `exp`.

Quando ligar:
- Apps com sessões longas (> 15 min) que precisam de logout server-side imediato.
- Compliance que exige revogação imediata em incidentes.

Como implementar:
- Adicionar claim `jti` ao token (`uuid4`) e armazenar `jti` revogados em Redis com
  TTL = `exp`. `decode_token` consulta o Redis e rejeita se `jti` revogado.
- Implementar `POST /auth/refresh` rotacionando refresh tokens com detecção de reuso.

### Sem account lockout incremental

Rate limit por IP cobre brute-force distribuído fracamente; brute-force por conta
ainda é possível em escala. Recomendado: contador de falhas por `user_id` com
backoff incremental (1s → 5s → 30s → bloqueio 15min).

### Sem 2FA / MFA

Considerar TOTP (RFC 6238) via `pyotp` quando a aplicação manipular dados sensíveis.
