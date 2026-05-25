# Deploy

Este diretório contém **templates** para publicar a API em provedores comuns. Nada está
ligado automaticamente — você escolhe um alvo, configura os secrets, remove o `if: false`
do workflow correspondente e o GitHub Actions cuida do resto.

| Provedor      | Workflow                                     | Diretório de apoio |
|---------------|----------------------------------------------|--------------------|
| Google Cloud Run | `.github/workflows/deploy-cloud-run.yml`  | `deploy/gcp/`      |
| AWS ECS Fargate  | `.github/workflows/deploy-aws-ecs.yml`    | `deploy/aws/`      |
| Vercel           | `.github/workflows/deploy-vercel.yml`     | `deploy/vercel/`   |

## Recomendação

| Caso de uso | Sugestão |
|-------------|----------|
| Quero começar barato e escalar zero-a-N | **Cloud Run** (Postgres = Cloud SQL ou Neon) |
| Quero algo na AWS com VPC, ALB, etc.    | **ECS Fargate** + RDS Postgres |
| Quero apenas demonstrar a API ao recrutador rapidamente | **Cloud Run** ou **Vercel** (atenção às limitações da Vercel — leia `deploy/vercel/README.md`) |

## Fluxo geral para ativar qualquer um dos templates

1. Provisione a infra fora do GitHub (cluster, registry, banco gerenciado).
2. Configure os secrets do workflow em `Settings → Secrets and variables → Actions`.
3. Remova `if: false` do job `deploy` no workflow correspondente.
4. Faça push em `main` (ou publique uma release) — o pipeline roda automático.

> ⚠️ **Nunca** coloque a `SECRET_KEY` em variável de ambiente plain no provedor.
> Use **Secret Manager** (GCP), **AWS Secrets Manager** ou o **Vercel Encrypted Env**.
