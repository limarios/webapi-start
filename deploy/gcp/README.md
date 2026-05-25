# Deploy · Google Cloud Run

## Pré-requisitos

- Projeto GCP com **billing** habilitado.
- APIs ativadas: `run.googleapis.com`, `artifactregistry.googleapis.com`, `sqladmin.googleapis.com`, `secretmanager.googleapis.com`.
- `gcloud` configurado localmente para a configuração inicial.

## Passo a passo

1. **Criar Artifact Registry**
   ```bash
   gcloud artifacts repositories create webapi-start \
     --repository-format=docker \
     --location=southamerica-east1
   ```

2. **Provisionar Cloud SQL Postgres** (ou usar [Neon](https://neon.tech) / [Supabase](https://supabase.com))
   ```bash
   gcloud sql instances create webapi-start-db \
     --database-version=POSTGRES_16 \
     --region=southamerica-east1 \
     --tier=db-f1-micro
   gcloud sql databases create webapi_start --instance=webapi-start-db
   ```

3. **Criar secrets**
   ```bash
   echo -n "$(python -c 'import secrets;print(secrets.token_urlsafe(64))')" | \
     gcloud secrets create APP_SECRET_KEY --data-file=-

   echo -n "postgresql+asyncpg://user:pass@/webapi_start?host=/cloudsql/<INSTANCE>" | \
     gcloud secrets create DATABASE_URL --data-file=-
   ```

4. **Configurar Workload Identity Federation** ([guia](https://github.com/google-github-actions/auth?tab=readme-ov-file#workload-identity-federation)).

5. **Definir os secrets no GitHub** conforme o workflow.

6. **Remover `if: false`** do job no workflow `.github/workflows/deploy-cloud-run.yml`.

## Custo aproximado (mínimo)

- Cloud Run scale-to-zero: ~US$ 0 ocioso, paga só pelo tráfego.
- Cloud SQL `db-f1-micro`: ~US$ 8/mês.
- Total: **~US$ 8/mês** com baixo tráfego — geralmente o mais barato para começar.
