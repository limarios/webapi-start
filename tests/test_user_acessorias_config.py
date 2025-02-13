import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_criar_config(ac_client: AsyncClient):
    response = await ac_client.post("/user_acessorias_config/", json={"login": "meulogin", "senha": "minhasenha"})
    assert response.status_code == 201
    assert response.json()["data"]["login"] == "meulogin"

@pytest.mark.asyncio
async def test_listar_configs(ac_client: AsyncClient):
    response = await ac_client.get("/user_acessorias_config/")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
