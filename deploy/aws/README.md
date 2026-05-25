# Deploy · AWS ECS Fargate

## Pré-requisitos

- Conta AWS com permissão para criar: ECR repository, ECS cluster + service, Task role, ALB, RDS Postgres.
- AWS CLI configurada localmente para a configuração inicial.

## Passo a passo (resumido)

1. **Provisionar o ECR**
   ```bash
   aws ecr create-repository --repository-name webapi-start --region sa-east-1
   ```

2. **Provisionar RDS Postgres** (ou Aurora Serverless v2)
   - Defina a senha forte e crie o database `webapi_start`.
   - Anote o endpoint para a `DATABASE_URL`.

3. **Criar Secrets Manager** com `SECRET_KEY` e `DATABASE_URL`.

4. **Criar ECS Cluster Fargate**
   ```bash
   aws ecs create-cluster --cluster-name webapi-start-cluster --region sa-east-1
   ```

5. **Registrar Task Definition inicial**
   - Edite `task-definition.json` substituindo `<ACCOUNT_ID>` e ARNs.
   - Registre:
     ```bash
     aws ecs register-task-definition --cli-input-json file://task-definition.json
     ```

6. **Criar Service** apontando para a task, atrás de um ALB.

7. **Configurar OIDC GitHub ↔ AWS** ([guia oficial](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)).

8. **Definir os secrets no GitHub** (veja o workflow `.github/workflows/deploy-aws-ecs.yml`).

9. **Remover `if: false`** do job `deploy` no workflow.

## Custo aproximado (mínimo)

- ECS Fargate 0.25 vCPU + 0.5 GB: ~US$ 8/mês
- RDS Postgres `db.t4g.micro`: ~US$ 12/mês
- ALB: ~US$ 18/mês
- Total: ~US$ 38/mês (sem free tier)
