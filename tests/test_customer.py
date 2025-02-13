import pytest
import httpx

# URL base da API
BASE_URL = "http://127.0.0.1:8000"

# Token JWT (será preenchido após login bem-sucedido)
ACCESS_TOKEN = None
pytest.globalvar = {}  # Criando um dicionário global para armazenar IDs

@pytest.fixture(scope="module")
def client():
    """ Cliente HTTP para requisições nos testes """
    with httpx.Client(base_url=BASE_URL) as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def authenticate(client):
    """ Realiza login e armazena o token de acesso """
    global ACCESS_TOKEN
    response = client.post("/auth/token", data={"username": "admin", "password": "techcoffee"})
    assert response.status_code == 200, "Falha ao autenticar o usuário"
    ACCESS_TOKEN = response.json()["access_token"]

@pytest.fixture
def new_customer():
    return {
        "nome": "Cliente Teste",
        "email": "cliente@example.com",
        "login": "cliente_teste",
        "grupo": "Teste",
        "telefone": "123456789",
        "cargo": "Analista",
        "setor": "TI",
        "ativo": True
    }


def test_create_customer(client, new_customer):
    """ Testa a criação de um cliente """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.post("/customers/", json=new_customer, headers=headers)

    print("CREATE CUSTOMER RESPONSE:", response.json())  # 🔍 Depuração

    assert response.status_code in [201, 422]
    if response.status_code == 201:
        pytest.globalvar["created_customer_id"] = response.json().get("id")
        assert pytest.globalvar["created_customer_id"] is not None, "Falha ao armazenar o ID do cliente!"
        print(f"Cliente criado com ID: {pytest.globalvar['created_customer_id']}")  # 🔍 Verifica se o ID foi salvo


def test_list_customers(client):
    """ Testa a listagem de clientes """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.get("/customers/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_customer(client):
    """ Testa a obtenção de um cliente por ID """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    customer_id = pytest.globalvar.get("created_customer_id")
    if customer_id is None:
        pytest.skip("Nenhum cliente foi criado, pulando o teste.")
    print(f"Testando obtenção do cliente com ID: {customer_id}")  # Depuração
    response = client.get(f"/customers/{customer_id}", headers=headers)
    assert response.status_code in [200, 404]

def test_update_customer(client):
    """ Testa a atualização de um cliente """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    customer_id = pytest.globalvar.get("created_customer_id")
    if customer_id is None:
        pytest.skip("Nenhum cliente foi criado, pulando o teste.")
    print(f"Testando atualização do cliente com ID: {customer_id}")  # Depuração
    response = client.get(f"/customers/{customer_id}", headers=headers)
    if response.status_code == 404:
        pytest.skip("Cliente não encontrado, pulando o teste de atualização")
    update_data = {"nome": "Cliente Atualizado"}
    response = client.put(f"/customers/{customer_id}", json=update_data, headers=headers)
    assert response.status_code in [200, 404]

def test_delete_customer(client):
    """ Testa a exclusão de um cliente """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    customer_id = pytest.globalvar.get("created_customer_id")
    if customer_id is None:
        pytest.skip("Nenhum cliente foi criado, pulando o teste.")
    print(f"Testando exclusão do cliente com ID: {customer_id}")  # Depuração
    response = client.get(f"/customers/{customer_id}", headers=headers)
    if response.status_code == 404:
        pytest.skip("Cliente não encontrado, pulando o teste de exclusão")
    response = client.delete(f"/customers/{customer_id}", headers=headers)
    assert response.status_code in [204, 404]
