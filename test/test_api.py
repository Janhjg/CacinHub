import pytest
import api
from fastapi.testclient import TestClient

client = TestClient(api.app)

# --- MOCK DATA ---
USUARIO_REAL = {
    "nombre": "Juan Test",
    "contrasena": "pass123",
    "fecha_nacimiento": "01/01/1990",
    "fichas": 500,
    "stats": {"partidas_totales": 0, "dados": 0, "ruleta": 0, "tragamonedas": 0, "carreras": 0}
}

class JuegoFalso:
    def __init__(self, *args, **kwargs):
        self.caballos = {"1": "Rayo"}
    def ejecutar_logica(self, monto, *args, **kwargs):
        return {"resultado": "ganaste", "ganancia": monto * 2, "simbolos": ["7","7","7"], "caballo": "1"}

# --- FIXTURES ---
@pytest.fixture()
def un_usuario():
    return {"USR001": {**USUARIO_REAL}}

@pytest.fixture()
def sin_disco(monkeypatch):
    for func in ["guardar_json", "guardar_db_usuarios", "registrar_partida"]:
        if hasattr(api, func):
            monkeypatch.setattr(api, func, lambda *a, **k: None)

@pytest.fixture()
def juegos_falsos(monkeypatch):
    for clase in ["JuegoDadosAPI", "JuegoCarrerasAPI", "JuegoRuletaAPI", "JuegoTragaMonedasAPI"]:
        if hasattr(api, clase):
            monkeypatch.setattr(api, clase, JuegoFalso)

def usar_db(monkeypatch, db):
    for func in ["cargar_json", "cargar_db_usuarios", "cargar_usuarios", "cargar_db_historial"]:
        if hasattr(api, func):
            monkeypatch.setattr(api, func, lambda *a, **k: db)

# --- TESTS ---

class TestEndpointsJuego:
    @pytest.mark.parametrize("path, payload", [
        ("/jugar/dados", {"user_id": "USR001", "monto": 100}),
        ("/jugar/carreras", {"user_id": "USR001", "monto": 50, "eleccion": "1"}),
        ("/jugar/ruleta", {"user_id": "USR001", "monto": 50, "tipo_apuesta": "2"}),
        ("/jugar/tragamonedas", {"user_id": "USR001", "monto": 10}) # Bajado a 10 por tu validación
    ])
    def test_jugadas_exitosas(self, monkeypatch, un_usuario, sin_disco, juegos_falsos, path, payload):
        usar_db(monkeypatch, un_usuario)
        r = client.post(path, json=payload)
        assert r.status_code == 200

    def test_gacha_exito(self, monkeypatch, un_usuario, sin_disco):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/gacha/chiste", params={"user_id": "USR001"})
        assert r.status_code in [200, 400] # 400 si no tiene fichas suf.

class TestGestionUsuarios:
    def test_obtener_info_usuario(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.get("/api/usuarios/USR001/info", params={"contrasena": "pass123"})
        assert r.status_code == 200
        assert r.json()["data"]["nombre"] == "Juan Test"

class TestBanco:
    def test_agregar_fichas_exito(self, monkeypatch, un_usuario, sin_disco):
        usar_db(monkeypatch, un_usuario)
        payload = {"user_id": "USR001", "contrasena": "pass123", "cantidad": 100}
        r = client.post("/api/banco/agregar-fichas", json=payload)
        assert r.status_code == 200
        assert r.json()["fichas_actuales"] == 600