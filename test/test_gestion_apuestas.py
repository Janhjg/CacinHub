import pytest
import api
from fastapi.testclient import TestClient

client = TestClient(api.app)

# ══════════════════════════════════════════════════════════════
# DATOS DE PRUEBA
# ══════════════════════════════════════════════════════════════

USUARIO_REAL = {
    "nombre": "Juan Test",
    "contrasena": "pass123",
    "fecha_nacimiento": "01/01/1990",
    "fichas": 500,
    "fecha_registro": "01/01/2024 00:00:00",
    "stats": {
        "partidas_totales": 0,
        "dados": 0,
        "ruleta": 0,
        "tragamonedas": 0,
        "carreras": 0
    }
}

# ══════════════════════════════════════════════════════════════
# CLASES FALSAS DE JUEGOS (reemplazan a las reales en los tests)
# ══════════════════════════════════════════════════════════════

class DadosFalso:
    def __init__(self, usuarios, uid, gestionar, guardar):
        self.usuarios = usuarios
        self.uid = uid
    def ejecutar_logica(self, monto):
        return {"resultado": "ganaste", "ganancia": monto * 2}

class CarrerasFalso:
    caballos = {"1": "Rayo", "2": "Trueno", "3": "Viento", "4": "Fuego"}
    def __init__(self, usuarios, uid, gestionar, guardar):
        pass
    def ejecutar_logica(self, monto, eleccion):
        return {"resultado": "ganaste", "caballo": eleccion}

class RuletaFalso:
    def __init__(self, usuarios, uid, gestionar, guardar):
        pass
    def ejecutar_logica(self, monto, tipo_apuesta, numero=None):
        return {"resultado": "numero", "numero_ganador": 7}

class TragaMonedasFalso:
    def __init__(self, usuarios, uid, gestionar, guardar):
        pass
    def ejecutar_logica(self, monto):
        return {"resultado": "jackpot", "ganancia": monto * 5}

# ══════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════

@pytest.fixture()
def un_usuario():
    return {"USR001": {**USUARIO_REAL}}

@pytest.fixture()
def sin_usuarios():
    return {}

@pytest.fixture()
def sin_disco(monkeypatch):
    """Evita que los tests escriban en disco."""
    monkeypatch.setattr(api, "guardar_json",     lambda path, data: None)
    monkeypatch.setattr(api, "guardar_usuarios", lambda data: None)

@pytest.fixture()
def juegos_falsos(monkeypatch):
    """Reemplaza todos los juegos reales por versiones controladas."""
    monkeypatch.setattr(api, "JuegoDadosAPI",        DadosFalso)
    monkeypatch.setattr(api, "JuegoCarrerasAPI",     CarrerasFalso)
    monkeypatch.setattr(api, "JuegoRuletaAPI",       RuletaFalso)
    monkeypatch.setattr(api, "JuegoTragaMonedasAPI", TragaMonedasFalso)

# ══════════════════════════════════════════════════════════════
# HELPER
# ══════════════════════════════════════════════════════════════

def usar_db(monkeypatch, db):
    """Inyecta una BD falsa en memoria para el test."""
    monkeypatch.setattr(api, "cargar_json",     lambda path: db)
    monkeypatch.setattr(api, "cargar_usuarios", lambda: db)

# ══════════════════════════════════════════════════════════════
# 1. POST /jugar/dados
# ══════════════════════════════════════════════════════════════

class TestDados:

    def test_jugada_correcta(self, monkeypatch, un_usuario, sin_disco, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/dados", json={"user_id": "USR001", "monto": 100})
        assert r.status_code == 200
        assert r.json()["resultado"] == "ganaste"

    def test_usuario_no_existe(self, monkeypatch, sin_usuarios):
        usar_db(monkeypatch, sin_usuarios)
        r = client.post("/jugar/dados", json={"user_id": "USR001", "monto": 100})
        assert r.status_code == 404
        assert "no encontrado" in r.json()["detail"].lower()

    def test_fichas_insuficientes(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/dados", json={"user_id": "USR001", "monto": 9999})
        assert r.status_code == 400
        assert "insuficientes" in r.json()["detail"].lower()

    def test_monto_exacto_al_saldo(self, monkeypatch, un_usuario, sin_disco, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/dados", json={"user_id": "USR001", "monto": 500})
        assert r.status_code == 200

    @pytest.mark.parametrize("monto", [1, 50, 250, 499])
    def test_montos_validos(self, monkeypatch, un_usuario, sin_disco, juegos_falsos, monto):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/dados", json={"user_id": "USR001", "monto": monto})
        assert r.status_code == 200


# ══════════════════════════════════════════════════════════════
# 2. POST /jugar/carreras
# ══════════════════════════════════════════════════════════════

class TestCarreras:

    @pytest.mark.parametrize("caballo", ["1", "2", "3", "4"])
    def test_caballo_valido(self, monkeypatch, un_usuario, sin_disco, juegos_falsos, caballo):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/carreras", json={"user_id": "USR001", "monto": 50, "eleccion": caballo})
        assert r.status_code == 200

    def test_usuario_no_existe(self, monkeypatch, sin_usuarios, juegos_falsos):
        usar_db(monkeypatch, sin_usuarios)
        r = client.post("/jugar/carreras", json={"user_id": "USR001", "monto": 50, "eleccion": "1"})
        assert r.status_code == 404

    def test_caballo_invalido(self, monkeypatch, un_usuario, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/carreras", json={"user_id": "USR001", "monto": 50, "eleccion": "99"})
        assert r.status_code == 400
        assert "caballo" in r.json()["detail"].lower()

    def test_eleccion_por_defecto(self, monkeypatch, un_usuario, sin_disco, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/carreras", json={"user_id": "USR001", "monto": 50})
        assert r.status_code == 200


# ══════════════════════════════════════════════════════════════
# 3. POST /jugar/ruleta
# ══════════════════════════════════════════════════════════════

class TestRuleta:

    def test_pleno_numero_valido(self, monkeypatch, un_usuario, sin_disco, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/ruleta", json={"user_id": "USR001", "monto": 100, "tipo_apuesta": "1", "numero": 17})
        assert r.status_code == 200

    def test_pleno_numero_cero(self, monkeypatch, un_usuario, sin_disco, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/ruleta", json={"user_id": "USR001", "monto": 100, "tipo_apuesta": "1", "numero": 0})
        assert r.status_code == 200

    def test_pleno_sin_numero(self, monkeypatch, un_usuario, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/ruleta", json={"user_id": "USR001", "monto": 100, "tipo_apuesta": "1"})
        assert r.status_code == 400

    @pytest.mark.parametrize("numero", [-1, 37, 100])
    def test_pleno_numero_fuera_de_rango(self, monkeypatch, un_usuario, juegos_falsos, numero):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/ruleta", json={"user_id": "USR001", "monto": 100, "tipo_apuesta": "1", "numero": numero})
        assert r.status_code == 400

    @pytest.mark.parametrize("tipo", ["2", "3"])
    def test_apuesta_color(self, monkeypatch, un_usuario, sin_disco, juegos_falsos, tipo):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/ruleta", json={"user_id": "USR001", "monto": 100, "tipo_apuesta": tipo})
        assert r.status_code == 200

    def test_usuario_no_existe(self, monkeypatch, sin_usuarios):
        usar_db(monkeypatch, sin_usuarios)
        r = client.post("/jugar/ruleta", json={"user_id": "USR001", "monto": 100, "tipo_apuesta": "2"})
        assert r.status_code == 404

    def test_fichas_insuficientes(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/ruleta", json={"user_id": "USR001", "monto": 9999, "tipo_apuesta": "2"})
        assert r.status_code == 400


# ══════════════════════════════════════════════════════════════
# 4. POST /jugar/tragamonedas
# ══════════════════════════════════════════════════════════════

class TestTragaMonedas:

    def test_jugada_correcta(self, monkeypatch, un_usuario, sin_disco, juegos_falsos):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/tragamonedas", json={"user_id": "USR001", "monto": 50})
        assert r.status_code == 200
        assert r.json()["resultado"] == "jackpot"

    def test_usuario_no_existe(self, monkeypatch, sin_usuarios):
        usar_db(monkeypatch, sin_usuarios)
        r = client.post("/jugar/tragamonedas", json={"user_id": "USR001", "monto": 50})
        assert r.status_code == 404

    def test_fichas_insuficientes(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.post("/jugar/tragamonedas", json={"user_id": "USR001", "monto": 9999})
        assert r.status_code == 400

    def test_juego_devuelve_error_retorna_400(self, monkeypatch, un_usuario):
        """Si el juego falla internamente, el endpoint debe devolver 400."""
        usar_db(monkeypatch, un_usuario)

        class JuegoRoto:
            def __init__(self, usuarios, uid, gestionar, guardar): pass
            def ejecutar_logica(self, monto):
                return {"error": "algo salio mal"}

        monkeypatch.setattr(api, "JuegoTragaMonedasAPI", JuegoRoto)
        r = client.post("/jugar/tragamonedas", json={"user_id": "USR001", "monto": 50})
        assert r.status_code == 400


# ══════════════════════════════════════════════════════════════
# 5. POST /api/usuarios  —  crear usuario
# ══════════════════════════════════════════════════════════════

class TestCrearUsuario:

    URL = "/api/usuarios"

    def test_creacion_exitosa(self, monkeypatch, sin_usuarios, sin_disco):
        usar_db(monkeypatch, sin_usuarios)
        r = client.post(self.URL, json={
            "nombre": "Ana García",
            "contrasena": "segura1",
            "fecha_nacimiento": "01/01/1994"
        })
        body = r.json()
        assert r.status_code == 200
        assert body["success"] is True
        assert "id" in body["data"]
        assert body["data"]["nombre"] == "Ana García"

    def test_nombre_muy_corto(self):
        r = client.post(self.URL, json={
            "nombre": "Ab",
            "contrasena": "segura1",
            "fecha_nacimiento": "01/01/1994"
        })
        assert r.json()["success"] is False
        assert "nombre" in r.json()["message"].lower()

    def test_contrasena_muy_corta(self):
        r = client.post(self.URL, json={
            "nombre": "Ana García",
            "contrasena": "abc",
            "fecha_nacimiento": "01/01/1994"
        })
        assert r.json()["success"] is False
        assert "contraseña" in r.json()["message"].lower()

    def test_fecha_invalida(self):
        r = client.post(self.URL, json={
            "nombre": "Ana García",
            "contrasena": "segura1",
            "fecha_nacimiento": "no-es-una-fecha"
        })
        assert r.json()["success"] is False
        assert "fecha" in r.json()["message"].lower()

    def test_menor_de_edad(self):
        r = client.post(self.URL, json={
            "nombre": "Ana García",
            "contrasena": "segura1",
            "fecha_nacimiento": "01/01/2015"
        })
        body = r.json()
        assert body["success"] is False
        assert "18" in body["message"]

    def test_respuesta_no_incluye_contrasena(self, monkeypatch, sin_usuarios, sin_disco):
        usar_db(monkeypatch, sin_usuarios)
        r = client.post(self.URL, json={
            "nombre": "Carlos Ruiz",
            "contrasena": "segura1",
            "fecha_nacimiento": "01/01/1990"
        })
        assert "contrasena" not in r.json().get("data", {})


# ══════════════════════════════════════════════════════════════
# 6. GET /api/usuarios  —  listar
# ══════════════════════════════════════════════════════════════

class TestListarUsuarios:

    URL = "/api/usuarios"

    def test_lista_vacia(self, monkeypatch, sin_usuarios):
        usar_db(monkeypatch, sin_usuarios)
        r = client.get(self.URL)
        body = r.json()
        assert r.status_code == 200
        assert body["success"] is True
        assert body["count"] == 0
        assert body["data"] == []

    def test_lista_un_usuario(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.get(self.URL)
        body = r.json()
        assert body["count"] == 1
        assert body["data"][0]["id"] == "USR001"
        assert body["data"][0]["nombre"] == "Juan Test"

    def test_lista_no_expone_contrasena(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.get(self.URL)
        for usuario in r.json()["data"]:
            assert "contrasena" not in usuario

    def test_lista_varios_usuarios(self, monkeypatch):
        db = {
            "USR001": {**USUARIO_REAL},
            "USR002": {**USUARIO_REAL, "nombre": "Sofía"},
            "USR003": {**USUARIO_REAL, "nombre": "Pedro"},
        }
        usar_db(monkeypatch, db)
        r = client.get(self.URL)
        assert r.json()["count"] == 3


# ══════════════════════════════════════════════════════════════
# 7. GET /api/usuarios/{user_id}/saldo
# ══════════════════════════════════════════════════════════════

class TestSaldo:

    def test_saldo_correcto(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.get("/api/usuarios/USR001/saldo", params={"contrasena": "pass123"})
        body = r.json()
        assert body["success"] is True
        assert body["data"]["fichas"] == 500
        assert body["data"]["nombre"] == "Juan Test"

    def test_usuario_no_existe(self, monkeypatch, sin_usuarios):
        usar_db(monkeypatch, sin_usuarios)
        r = client.get("/api/usuarios/USR001/saldo", params={"contrasena": "pass123"})
        assert r.json()["success"] is False
        assert "no encontrado" in r.json()["message"].lower()

    def test_contrasena_incorrecta(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.get("/api/usuarios/USR001/saldo", params={"contrasena": "MALA"})
        body = r.json()
        assert body["success"] is False
        assert "contraseña" in body["message"].lower()

    def test_respuesta_no_expone_contrasena(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.get("/api/usuarios/USR001/saldo", params={"contrasena": "pass123"})
        assert "contrasena" not in r.json().get("data", {})


# ══════════════════════════════════════════════════════════════
# 8. GET /api/usuarios/{user_id}/info
# ══════════════════════════════════════════════════════════════

class TestInfoCompleta:

    def test_info_correcta(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.get("/api/usuarios/USR001/info", params={"contrasena": "pass123"})
        body = r.json()
        assert body["success"] is True
        for campo in ("fichas", "fecha_nacimiento", "fecha_registro", "stats"):
            assert campo in body["data"]

    def test_usuario_no_existe(self, monkeypatch, sin_usuarios):
        usar_db(monkeypatch, sin_usuarios)
        r = client.get("/api/usuarios/USR001/info", params={"contrasena": "pass123"})
        assert r.json()["success"] is False

    def test_contrasena_incorrecta(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.get("/api/usuarios/USR001/info", params={"contrasena": "MALA"})
        body = r.json()
        assert body["success"] is False
        assert "contraseña" in body["message"].lower()

    def test_respuesta_no_expone_contrasena(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.get("/api/usuarios/USR001/info", params={"contrasena": "pass123"})
        assert "contrasena" not in r.json().get("data", {})


# ══════════════════════════════════════════════════════════════
# 9. POST /api/banco/agregar-fichas
# ══════════════════════════════════════════════════════════════

class TestAgregarFichas:

    URL = "/api/banco/agregar-fichas"

    def payload(self, cantidad=200, user_id="USR001", contrasena="pass123"):
        return {"user_id": user_id, "contrasena": contrasena, "cantidad": cantidad}

    def test_agregar_exitoso(self, monkeypatch, un_usuario, sin_disco):
        usar_db(monkeypatch, un_usuario)
        r = client.post(self.URL, json=self.payload(200))
        body = r.json()
        assert body["success"] is True
        assert body["data"]["fichas_antes"]     == 500
        assert body["data"]["fichas_agregadas"] == 200
        assert body["data"]["fichas_despues"]   == 700

    def test_usuario_no_existe(self, monkeypatch, sin_usuarios):
        usar_db(monkeypatch, sin_usuarios)
        r = client.post(self.URL, json=self.payload(100, user_id="NOEXISTE"))
        assert r.json()["success"] is False
        assert "no encontrado" in r.json()["message"].lower()

    def test_contrasena_incorrecta(self, monkeypatch, un_usuario):
        usar_db(monkeypatch, un_usuario)
        r = client.post(self.URL, json=self.payload(100, contrasena="MALA"))
        body = r.json()
        assert body["success"] is False
        assert "contraseña" in body["message"].lower()

    @pytest.mark.parametrize("cantidad", [0, -1, -500])
    def test_cantidad_no_positiva(self, monkeypatch, un_usuario, cantidad):
        usar_db(monkeypatch, un_usuario)
        r = client.post(self.URL, json=self.payload(cantidad))
        assert r.json()["success"] is False
        assert "mayor a 0" in r.json()["message"]

    def test_saldo_final_correcto(self, monkeypatch, sin_disco):
        db = {"USR001": {**USUARIO_REAL, "fichas": 300}}
        usar_db(monkeypatch, db)
        r = client.post(self.URL, json=self.payload(150))
        assert r.json()["data"]["fichas_despues"] == 450

    def test_respuesta_incluye_nombre(self, monkeypatch, un_usuario, sin_disco):
        usar_db(monkeypatch, un_usuario)
        r = client.post(self.URL, json=self.payload(50))
        assert r.json()["data"]["nombre"] == "Juan Test"










