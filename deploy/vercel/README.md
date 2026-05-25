# Deploy · Vercel

⚠️ **Atenção:** a Vercel **não** é o alvo ideal para uma API FastAPI completa com Postgres
persistente. Limitações relevantes:

- Serverless cold-start em cada requisição.
- Sem state local (cada request roda em uma sandbox).
- Conexões com Postgres precisam usar **pooling externo** (PgBouncer, Neon serverless driver).
- Tamanho de payload e duração de função limitados.

Use Cloud Run ou AWS ECS para produção real. **Vercel serve só para demos rápidas**.

## Estrutura mínima para rodar FastAPI na Vercel

Crie `vercel.json` na raiz:

```json
{
  "version": 2,
  "builds": [
    { "src": "app/main.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "app/main.py" }
  ]
}
```

E configure variáveis de ambiente no painel da Vercel:

- `SECRET_KEY`
- `DATABASE_URL` (ex: Neon ou Supabase)
- `APP_ENV=production`
- `LOG_JSON=true`

## Passo a passo

1. Crie projeto em [vercel.com/new](https://vercel.com/new).
2. Crie um banco Postgres serverless ([Neon](https://neon.tech) recomendado).
3. Em `Settings → Environment Variables` configure os secrets acima.
4. Defina os secrets no GitHub (`VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`).
5. Remova `if: false` do workflow `.github/workflows/deploy-vercel.yml`.
