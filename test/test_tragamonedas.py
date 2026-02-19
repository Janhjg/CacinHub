import pytest
from fastapi.testclient import TestClient
import api
import random

client = TestClient(api.app)

@pytest.fixture
def db_kaiji():
    return {
        "6969": {
            "nombre": "Kaiji Itou",
            "contrasena": "1234",
            "fichas": 100,  
            "stats": {"partidas_totales": 0, "tragamonedas": 0}
        }
    }

def test_tragamonedas_jackpot(monkeypatch, db_kaiji):
    """JACKPOT 7-7-7"""
    monkeypatch.setattr(api, "cargar_json", lambda path: db_kaiji)
    monkeypatch.setattr(api, "guardar_json", lambda path, data: None)

    monkeypatch.setattr(random, "randint", lambda a, b: 7)

    payload = {"user_id": "6969", "monto": 10}
    response = client.post("/jugar/tragamonedas", json=payload)

    assert response.status_code == 200
    data = response.json()
    
    assert data["resultado"] == "gano"
    assert data["fichas_finales"] == 990
    assert "ENHORABUENA" in data["detalles"]

def test_tragamonedas_perdida(monkeypatch, db_kaiji):
    monkeypatch.setattr(api, "cargar_json", lambda path: db_kaiji)
    
    resultados = iter([1, 2, 3])
    monkeypatch.setattr(random, "randint", lambda a, b: next(resultados))

    payload = {"user_id": "6969", "monto": 10}
    response = client.post("/jugar/tragamonedas", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["resultado"] == "perdio"

    assert data["fichas_finales"] == 90
    assert "MANUTENCION" in data["detalles"]

def test_tragamonedas_limite_apuesta(monkeypatch, db_kaiji):
    monkeypatch.setattr(api, "cargar_json", lambda path: db_kaiji)

    payload = {"user_id": "6969", "monto": 50}
    response = client.post("/jugar/tragamonedas", json=payload)

    assert response.status_code == 400
    assert "ELEVADA" in response.json()["detail"]