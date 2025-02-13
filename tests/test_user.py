import pytest
import httpx

# URL base da API
BASE_URL = "http://127.0.0.1:8000"

# Usuário de teste ajustado conforme a API
TEST_USER = {
    "username": "testuser",
    "password": "testpassword",
    "email": "testuser@example.com",
    "full_name": "Test User",
    "cargo": "Desenvolvedor",
    "grupo": "Usuário"
}

# Token JWT (será preenchido após login bem-sucedido)
ACCESS_TOKEN = None


@pytest.fixture(scope="module")
def client():
    """ Cliente HTTP para requisições nos testes """
    with httpx.Client(base_url=BASE_URL) as client:
        yield client


def test_create_user(client):
    """ Testa a criação de um usuário """
    response = client.post("/users/", json=TEST_USER)
    print("CREATE USER RESPONSE:", response.json())

    assert response.status_code in [201, 422]  # Pode ser criado ou erro de validação
    if response.status_code == 201:
        json_data = response.json()
        assert "login" in json_data  # API usa "login" ao invés de "username"


def test_login(client):
    """ Testa o login e a obtenção do token JWT """
    global ACCESS_TOKEN
    response = client.post("/auth/token", data={"username": "admin", "password": "techcoffee"})

    print("LOGIN RESPONSE:", response.json())
    assert response.status_code == 200  # OK

    json_data = response.json()
    assert "access_token" in json_data
    ACCESS_TOKEN = json_data["access_token"]


def test_get_current_user(client):
    """ Testa a obtenção do usuário autenticado """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.get("/users/me", headers=headers)
    json_data = response.json()

    print("CURRENT USER RESPONSE:", json_data)
    assert response.status_code == 200  # OK

    # Verificar os campos corretos conforme a resposta da API
    assert all(
        k in json_data for k in ["nome", "email", "login", "cargo"]), "A resposta da API não contém os campos esperados"


def test_list_users(client):
    """ Testa a listagem de usuários (rota protegida) """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.get("/users/", headers=headers)

    print("LIST USERS RESPONSE:", response.json())
    assert response.status_code == 200  # OK
    assert isinstance(response.json(), list)


def test_get_user_by_id(client):
    """ Testa a obtenção de um usuário específico """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.get("/users/1", headers=headers)
    json_data = response.json()

    print("GET USER BY ID RESPONSE:", json_data)
    assert response.status_code in [200, 404]  # Pode retornar OK ou Não Encontrado

    if response.status_code == 200:
        assert all(
            k in json_data for k in ["nome", "email", "cargo"]), "A resposta da API não contém os campos esperados"


def test_update_user(client):
    """ Testa a atualização dos dados do usuário """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = client.get("/users/1", headers=headers)
    if response.status_code == 404:
        pytest.skip("Usuário não encontrado, pulando o teste de atualização")

    update_data = {"email": "updated@example.com"}
    response = client.put("/users/1", json=update_data, headers=headers)

    print("UPDATE USER RESPONSE:", response.status_code, response.text)  # 🔍 Log detalhado

    assert response.status_code in [200, 404], f"Erro inesperado: {response.text}"

    if response.status_code == 200:
        try:
            json_data = response.json()
            assert json_data["email"] == "updated@example.com"
        except Exception as e:
            pytest.fail(f"Erro ao processar resposta JSON: {e}")


def test_delete_user(client):
    """ Testa a exclusão de um usuário """
    assert ACCESS_TOKEN is not None, "Token JWT não foi gerado no login!"

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    # ✅ Verifica se o usuário existe antes de deletar
    response = client.get("/users/10", headers=headers)
    if response.status_code == 404:
        pytest.skip("Usuário não encontrado, pulando o teste de exclusão")

    response = client.delete("/users/10", headers=headers)

    print("DELETE USER RESPONSE:", response.text)  # Captura a resposta bruta para depuração
    assert response.status_code in [204, 404]  # Pode ser sucesso ou usuário não encontrado

