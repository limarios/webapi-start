### 🚀 API Start

### 📌 Descrição

Esta API foi desenvolvida como projeto start e serve como o núcleo central para desenvolvimento de API. 

Baseada em princípios modernos, como **Clean Architecture** e **Domain-Driven Design(DDD)**, a API integra, gerencia e orquestra processos gerais de uma API completa. Projetada para ser **flexível, robusta e escalável**, ela permite a evolução contínua e a integração com sistemas legados e futuros, garantindo segurança, desempenho e manutenibilidade em suas operações.


---

## 📖 Índice

1. [🚀 Tecnologias Utilizadas](#-tecnologias-utilizadas)
2. [🛠️ Instalação e Configuração](#️-instalação-e-configuração)
3. [📦 Recursos](#️-recursos)
4. [🔧 Estrutura do Projeto](#-estrutura-do-projeto)
5. [📡 Executando a API](#-executando-a-api)
6. [📝 Endpoints Disponíveis](#-endpoints-disponíveis)
7. [🔑 Autenticação e Segurança](#-autenticação-e-segurança)
8. [🛠️ Contribuição](#️-contribuição)
9. [📜 Licença](#-licença)
10. [📩 Contato](#-contato)

---

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework:** FastAPI
- **Banco de Dados:** MySQL
- **ORM:** SQLAlchemy + Alembic (para migrations)
- **Autenticação:** OAuth2 + JWT
- **Documentação:** OpenAPI / Swagger UI
- **Ferramentas de Testes:** Pytest
- **Ferramentas de Log:** Loguru
- **Gerenciador de Dependências:** Poetry / Pipenv
- **Coletor de métricas:** Prometheus
- **Dashboard de monitoramento:** Grafana
- **Containerização:** Docker + Docker Compose (opcional)

---

## 📦 Recursos

- **Gerenciamento de Usuários:** Criação, leitura, atualização e deleção de usuários.
- **Gerenciamento de Clientes:** Operações CRUD para clientes, com validações e regras de negócio.
- **Gerenciamento de Atividades:** Criação, listagem, atualização e remoção de atividades.
- **Documentação Interativa:** Swagger UI e ReDoc integrados para facilitar o entendimento e a experimentação dos endpoints.


---

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.9 ou superior instalado.
- MySQL instalado e configurado (ou outro banco de dados compatível).
- Ambiente virtual (recomendado).

### Passos

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Matlima/webapi-start
   cd webapi-start
   ```

2. **Crie ative um ambiente virtual:**
    
    ```bash 
      python -m venv venv
       # No Windows:
       venv\Scripts\activate
       # No macOS/Linux:
       source venv/bin/activate
    ```
   
3. **Instalando as dependências**
   ```bash 
      pip install -r requirements.txt
   ```


4. **Configurando o arquivo .env**
3 arquivos de ``.env`` um padrão, ambiente de desenvolvimento e produção para ter uma base como esta sendo operado, a ``SECRET_KEY`` usada é a de teste, alterar após clonar repositório.

</br> Crie um arquivo ``.env`` na raiz do projeto e configure suas variáveis de ambiente:
   ```bash 
      DB_USER=root
      DB_PASS=
      DB_HOST=localhost
      DB_PORT=3306
      DB_NAME=seu_database
      SECRET_KEY="sua_chave_secreta"
      ALGORITHM="HS256"
      ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Criar as tabelas no banco de dados**
   ```bash 
      alembic upgrade head
   ```

---

## 🔧 Estrutura do Projeto

```bash 
   alcance-api/
│── app/
│   ├── api/                      # Interface da aplicação (Interface Adapters)
│   │   ├── v1/                   # Versão da API
│   │   │   ├── endpoints/        # Endpoints da API
│   │   │   │   ├── routes.py     # Definição de todas as rotas
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py   # Dependências comuns (ex: autenticação)
│   ├── core/                     # Configurações principais e segurança
│   │   ├── auth.py               # Lógica de autenticação e segurança
│   │   ├── token.py              # Gerenciamento de tokens JWT
│   │   ├── config.py             # Configurações globais (ex: .env)
│   ├── db/                       # Infraestrutura do banco de dados
│   │   ├── session.py            # Gerenciamento da sessão do banco
│   │   ├── base_class.py               # Base para os modelos SQLAlchemy
│   │   ├── migrations/           # Migrações do banco de dados (Alembic)
│   ├── infra/                    # Gerencia persistência de dados, logs e serviços de suporte como monitoramento.
│   │   ├── health.py             # Implementa o endpoint de verificação de saúde da API.
│   │   ├── logger.py             # Configuração centralizada de logs.
│   │   ├── middleware.py         # Implementação de middlewares da API.
│   │   ├── monitoring.py         # Integração com Prometheus e Grafana para métricas.
│   ├── domain/                   # Camada de Domínio (DDD)
│   │   ├── auth/                 # Domínio de autenticação
│   │   │   ├── routes.py         # Rotas relacionadas à autenticação
│   │   │   ├── service.py        # Lógica de autenticação (caso de uso)
│   │   │   ├── repository.py     # Acesso ao banco de dados
│   │   │   ├── schemas.py        # Esquemas Pydantic para validação
│   │   ├── user/                 # Domínio de Usuários
│   │   │   ├── routes.py         # Rotas dos usuários
│   │   │   ├── service.py        # Lógica de negócios
│   │   │   ├── repository.py     # Repositório (acesso ao banco)
│   │   │   ├── schemas.py        # Validações e serializações
│   │   ├── customer/             # Domínio de Clientes
│   │   │   ├── routes.py         # Rotas dos clientes
│   │   │   ├── service.py        # Lógica de negócios
│   │   │   ├── repository.py     # Repositório (acesso ao banco)
│   │   │   ├── schemas.py        # Validações e serializações
│   │   ├── activity/             # Domínio de Atividades
│   │   │   ├── routes.py         # Rotas das atividades
│   │   │   ├── service.py        # Lógica de negócios
│   │   │   ├── repository.py     # Repositório (acesso ao banco)
│   │   │   ├── schemas.py        # Validações e serializações
│   ├── logs/                     # Logs da aplicação
│   ├── tests/                    # Testes automatizados
│   │   ├── test_auth.py          # Testes de autenticação
│   │   ├── test_users.py         # Testes de usuários
│   │   ├── test_customers.py     # Testes de clientes
│   │   ├── test_activities.py    # Testes de atividades
│   ├── main.py                   # Ponto de entrada da API
│── .env                          # Variáveis de ambiente
│── requirements.txt              # Dependências do projeto
│── alembic.ini                   # Configuração do Alembic
│── README.md                     # Documentação do projeto
│── docker-compose.yml            # Configuração Docker Compose (opcional)
 ```

---

## 📡 Executando a API

### 🔹 Executar localmente
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
### 🔹 Executar com Docker
```bash
docker-compose up --build
```

### 🔹 Acessar a documentação interativa
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

---

## 📝 Endpoints Disponíveis

### 🔹Usuários
- **Criar usuário:** ``POST /users/``
- **Listar usuários:** ``GET /users/users_all``
- **Buscar usuário por ID:** ``GET /users/{user_id}``
- **Atualizar usuário:** ``PUT /users/{user_id}``
- **Excluir usuário: DELETE** ``/users/{user_id}``

### 🔹 Clientes
- **Criar cliente:** ``POST /customers/``
- **Listar clientes:** ``GET /customers/``
- **Buscar cliente por ID:** ``GET /customers/{customer_id}``
- **Atualizar cliente:** ``PUT /customers/{customer_id}``
- **Excluir cliente:** ``DELETE /customers/{customer_id}``

### 🔹 Atividades
- **Criar atividade:** ``POST /activities/``
- **Listar atividades:** ``GET /activities/``
- **Buscar atividade por ID:** ``GET /activities/{activity_id}``
- **Atualizar atividade:** ``PUT /activities/{activity_id}``
- **Excluir atividade:** ``DELETE /activities/{activity_id}``

---

## 🔑 Autenticação e Segurança

#### A API utiliza OAuth2 com JWT (JSON Web Token) para autenticação.

1. Para autenticar, faça login enviando um ``POST`` para ``/auth/token`` com:
```bash
{
  "username": "usuario@example.com",
  "password": "sua_senha"
}
```

2. Use o token JWT recebido para acessar os endpoints protegidos:
```bash
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/users/
```

---

## 🛠️ Contribuição

Se quiser contribuir com melhorias, siga estas etapas:

- Fork o repositório
- Crie um ***branch*** (```git checkout -b feature/nova-feature```)
- ***Commit*** suas alterações (``git commit -m 'Adiciona nova feature``)
- ***Push*** para o branch (``git push origin feature/nova-feature``)
- Abra um ***Pull Request***

---

## 📜 Licença

Este projeto está licenciado sob a MIT License - consulte o arquivo LICENSE para mais detalhes.

---

## 📩 Contato

- Desenvolvido por: Matheus de Lima Rios
- Site: https://agenciatechcoffee.com

---

## 🔹 **Como usar o `README.md`**

1. **Expanda a documentação** conforme novas funcionalidades forem adicionadas.
2. **Adicione mais detalhes sobre os endpoints** conforme necessário.
3. **Mantenha atualizado** com mudanças na API.

Esse modelo segue **boas práticas** para documentação de APIs e pode ser facilmente mantido e atualizado conforme a API evolui. 
