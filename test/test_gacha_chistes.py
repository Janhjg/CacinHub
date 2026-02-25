import pytest
from fastapi.testclient import TestClient
import api
import random

client = TestClient(api.app)

@pytest.fixture
def db_ricardo():
    """Estado inicial de Ricardo antes de su adicción a los chistes."""
    return {
        "1111": {
            "nombre": "Ricardo",
            "contrasena": "abcd",
            "fichas": 10, 
            "stats": {"partidas_totales": 0}
        }
    }

def test_gacha_exito(monkeypatch, db_ricardo):
    """Prueba que puede canjear un chiste y se le descuentan 5 fichas."""
    monkeypatch.setattr(api, "cargar_json", lambda path: db_ricardo)
    monkeypatch.setattr(api, "guardar_json", lambda path, data: None)

    chiste_fijo = "¿Qué hace una abeja en el gimnasio? ¡Zumba!"
    monkeypatch.setattr(random, "choice", lambda lista: chiste_fijo)

    response = client.post(f"/gacha/chiste?user_id=1111")

    assert response.status_code == 200
    data = response.json()
    assert data["resultado"] == "éxito"
    assert data["chiste"] == chiste_fijo
    assert data["fichas_restantes"] == 5  # 10 iniciales - 5 del costo

def test_gacha_insuficiente(monkeypatch, db_ricardo):
    """Prueba que recibe un error si solo tiene 2 fichas."""
    # Modificamos a Ricardo para que sea pobre
    db_ricardo["1111"]["fichas"] = 2
    monkeypatch.setattr(api, "cargar_json", lambda path: db_ricardo)

    response = client.post(f"/gacha/chiste?user_id=1111")

    assert response.status_code == 400
    assert "insuficientes" in response.json()["detail"].lower()

def test_gacha_usuario_no_existe(monkeypatch):
    """Prueba que la API responde 404 si el ID no existe."""
    monkeypatch.setattr(api, "cargar_json", lambda path: {})

    response = client.post(f"/gacha/chiste?user_id=9999")

    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"].lower()