import pytest
from fastapi.testclient import TestClient
import api

client = TestClient(api.app)

@pytest.fixture
def db_kiryu():
    """Simula el estado inicial de Kiryu en el casino."""
    return {
        "6767": {
            "nombre": "Kazuma Kiryu",
            "contrasena": "1234",
            "fecha_nacimiento": "17/06/1968",
            "fichas": 1000,
            "stats": {"partidas_totales": 0, "carreras": 0}
        }
    }

def test_apuesta_valida_kiryu(monkeypatch, db_kiryu):
    """Prueba una apuesta normal de Kiryu."""
    monkeypatch.setattr(api, "cargar_json", lambda path: db_kiryu)
    monkeypatch.setattr(api, "guardar_json", lambda path, data: None)

    payload = {
        "user_id": "6767",
        "monto": 100,
        "eleccion": "1"
    }

    response = client.post("/jugar/carreras", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["juego"] == "carreras"
    assert "tu_caballo" in data
    assert "ganador" in data

def test_kiryu_sin_fichas(monkeypatch, db_kiryu):
    """Prueba que Kiryu no puede apostar más de lo que tiene."""
    monkeypatch.setattr(api, "cargar_json", lambda path: db_kiryu)

    payload = {
        "user_id": "6767",
        "monto": 99999,  # Más de sus 1000 fichas
        "eleccion": "1"
    }

    response = client.post("/jugar/carreras", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Fichas insuficientes"

def test_caballo_inexistente(monkeypatch, db_kiryu):
    """Prueba error al elegir un caballo que no está en la lista."""
    monkeypatch.setattr(api, "cargar_json", lambda path: db_kiryu)

    payload = {
        "user_id": "6767",
        "monto": 50,
        "eleccion": "9"  # No existe el caballo 9
    }

    response = client.post("/jugar/carreras", json=payload)
    
    assert response.status_code == 400
    assert "no existe" in response.json()["detail"].lower()

def test_usuario_desconocido(monkeypatch):
    """Prueba error cuando el ID no existe en la base de datos."""
    monkeypatch.setattr(api, "cargar_json", lambda path: {})

    payload = {
        "user_id": "0000",
        "monto": 10,
        "eleccion": "1"
    }

    response = client.post("/jugar/carreras", json=payload)
    
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"].lower()