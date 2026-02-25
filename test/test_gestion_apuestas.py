import pytest
import api
from fastapi.testclient import TestClient

client = TestClient(api.app)

# --- DATOS DE PRUEBA ---

USUARIO_REAL = {
    "nombre": "Juan Test",
    "contrasena": "pass123",
    "fecha_nacimiento": "01/01/1990",
    "fichas": 500,
    "fecha_registro": "01/01/2024 00:00:00",
    "stats": {
        "partidas_totales": 0,
        "dados": 0, "ruleta": 0, "tragamonedas": 0, "carreras": 0
    }
}

# --- CLASES FALSAS ---

class JuegoBaseFalso:
    def __init__(self, *args, **kwargs):
        self.caballos = {"1": "Caballo 1", "2": "Caballo 2", "3": "Caballo 3", "4": "Caballo 4"}
        self.opciones_ruleta = {"1": "Rojo", "2": "Negro"}
        
    def ejecutar_logica(self, *args, **kwargs):
        return {
            "resultado": "ganaste", 
            "ganancia": 100, 
            "caballo": "1", 
            "numero_ganador": 7, 
            "simbolos": ["7", "7", "7"]
        }

# --- FIXTURES ---

@pytest.fixture()
def un_usuario():
    return {"USR001": {**USUARIO_REAL}}

@pytest.fixture()
def sin_usuarios():
    return {}

@pytest.fixture()
def sin_disco(monkeypatch):
    """Evita escritura en archivos reales."""
    funciones = ["guardar_json", "guardar_db_usuarios", "guardar_usuarios", "registrar_partida"]
    for func in funciones:
        if hasattr(api, func):
            monkeypatch.setattr(api, func, lambda *a, **k: None)

@pytest.fixture()
def juegos_falsos(monkeypatch):
    """Simula las clases de juego."""
    clases = ["JuegoDadosAPI", "JuegoCarrerasAPI", "JuegoRuletaAPI", "JuegoTragaMonedasAPI"]
    for clase in clases:
        if hasattr(api, clase):
            monkeypatch.setattr(api, clase, JuegoBaseFalso)

def usar_db(monkeypatch, db):
    """Inyecta la base de datos ficticia."""
    if hasattr(api, "cargar_json"):
        monkeypatch.setattr(api, "cargar_json", lambda path: db)
    
    for func in ["cargar_usuarios", "cargar_db_usuarios", "cargar_datos"]:
        if hasattr(api, func):
            monkeypatch.setattr(api, func, lambda *a: db)

# --- TESTS CORREGIDOS ---

class TestApuestas:
    def test_dados_exitoso(self, monkeypatch, un_usuario, sin_disco, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/dados", json={"user_id": "USR001", "monto": 100})
        assert r.status_code == 200

    def test_carreras_caballo_invalido(self, monkeypatch, un_usuario, sin_disco, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/carreras", json={"user_id": "USR001", "monto": 50, "eleccion": "99"})
        assert r.status_code == 400

    def test_fichas_insuficientes(self, monkeypatch, un_usuario, sin_disco):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/dados", json={"user_id": "USR001", "monto": 9999})
        assert r.status_code == 400

class TestUsuarios:
    def test_crear_nombre_corto(self, monkeypatch, sin_usuarios, sin_disco):
        usar_db(monkeypatch, sin_usuarios)
        r = client.post("/api/usuarios", json={
            "nombre": "Ab", "contrasena": "123456", "fecha_nacimiento": "01/01/1990"
        })
        assert r.status_code == 400

    def test_menor_de_edad(self, monkeypatch, sin_usuarios, sin_disco):
        usar_db(monkeypatch, sin_usuarios)
        r = client.post("/api/usuarios", json={
            "nombre": "Usuario Joven", "contrasena": "123456", "fecha_nacimiento": "01/01/2015"
        })
        assert r.status_code == 403

class TestBanco:
    def test_agregar_fichas_usuario_inexistente(self, monkeypatch, sin_usuarios, sin_disco):
        usar_db(monkeypatch, sin_usuarios)
        payload = {"user_id": "NO_EXISTE", "contrasena": "pass123", "cantidad": 100}
        r = client.post("/api/banco/agregar-fichas", json=payload)
        
        assert r.status_code == 401
        assert r.json()["detail"] == "Credenciales inválidas"

    def test_agregar_fichas_cantidad_negativa(self, monkeypatch, un_usuario, sin_disco):
        usar_db(monkeypatch, un_usuario)
        payload = {"user_id": "USR001", "contrasena": "pass123", "cantidad": -50}
        r = client.post("/api/banco/agregar-fichas", json=payload)
        assert r.status_code == 400
        assert "positiva" in r.json()["detail"]