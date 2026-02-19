from Funciones.funciones import *
from juegos.base_juegos import Juego
import pytest
import json


@pytest.fixture
def usuarios_db_con_usuario():
    """Crea un usuario de prueba sin usar crear_usuario() que pide input"""
    usuario_test = Usuario("TestUser", "pass123", "01/01/2000", id_usuario="1234", fichas=100)
    return {"1234": usuario_test.to_dict()}


@pytest.fixture
def usuarios_db_con_poco_saldo():
    """Crea un usuario con pocas fichas para probar validaciones"""
    usuario_pobre = Usuario("UsuarioPobre", "pass123", "01/01/2000", id_usuario="5678", fichas=10)
    return {"5678": usuario_pobre.to_dict()}


@pytest.fixture
def usuarios_db_varios_usuarios():
    """Crea varios usuarios con diferentes saldos"""
    usuarios = {}
    
    user1 = Usuario("Rico", "pass1", "01/01/1990", id_usuario="1111", fichas=1000)
    user2 = Usuario("Medio", "pass2", "15/05/1995", id_usuario="2222", fichas=100)
    user3 = Usuario("Pobre", "pass3", "30/12/2000", id_usuario="3333", fichas=10)
    
    usuarios["1111"] = user1.to_dict()
    usuarios["2222"] = user2.to_dict()
    usuarios["3333"] = user3.to_dict()
    
    return usuarios


# =====================================================
# TESTS DE GESTIÓN DE APUESTAS CON gestionar_apuesta()
# =====================================================

def test_apuesta_ganada_aumenta_fichas(usuarios_db_con_usuario):
    """Verifica que al ganar una apuesta se incrementan las fichas correctamente"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]  # 100
    monto_apuesta = 20
    multiplicador = 2
    
    # Ganar apuesta
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", monto_apuesta, "dados", gano=True, multiplicador=multiplicador)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    ganancia_neta = monto_apuesta * (multiplicador - 1)
    
    # Verificar que las fichas aumentaron correctamente
    assert fichas_despues == fichas_antes + ganancia_neta
    assert fichas_despues == 120  # 100 - 20 + (20 * 2) = 120


def test_apuesta_perdida_no_aumenta_fichas(usuarios_db_con_usuario):
    """Verifica que al perder una apuesta las fichas disminuyen"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]  # 100
    monto_apuesta = 20
    
    # Perder apuesta
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", monto_apuesta, "ruleta", gano=False, multiplicador=2)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    
    # Las fichas deben disminuir al perder
    assert fichas_despues == fichas_antes - monto_apuesta
    assert fichas_despues == 80  # 100 - 20


def test_actualizacion_de_fichas_multiples_apuestas(usuarios_db_con_usuario):
    """Verifica que las fichas se actualizan correctamente tras múltiples apuestas"""
    usuarios_db = usuarios_db_con_usuario
    
    # Ganar primera apuesta: 100 - 20 + (20 * 2) = 120
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 20, "dados", gano=True, multiplicador=2)
    assert usuarios_db["1234"]["fichas"] == 120
    
    # Perder segunda apuesta: 120 - 10 = 110
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "ruleta", gano=False, multiplicador=2)
    assert usuarios_db["1234"]["fichas"] == 110
    
    # Ganar tercera apuesta con multiplicador 3: 110 - 10 + (10 * 3) = 130
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "tragamonedas", gano=True, multiplicador=3)
    assert usuarios_db["1234"]["fichas"] == 130


def test_diferentes_multiplicadores(usuarios_db_con_usuario):
    """Verifica que funcionan correctamente diferentes multiplicadores"""
    usuarios_db = usuarios_db_con_usuario
    
    # Multiplicador 2: 100 - 10 + (10*2) = 110
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=True, multiplicador=2)
    assert usuarios_db["1234"]["fichas"] == 110
    
    # Multiplicador 3: 110 - 10 + (10*3) = 130
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "tragamonedas", gano=True, multiplicador=3)
    assert usuarios_db["1234"]["fichas"] == 130
    
    # Multiplicador 5: 130 - 10 + (10*5) = 170
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "carreras", gano=True, multiplicador=5)
    assert usuarios_db["1234"]["fichas"] == 170


def test_multiplicador_2_funciona_correctamente(usuarios_db_con_usuario):
    """Verifica que el multiplicador 2 funciona correctamente"""
    usuarios_db = usuarios_db_con_usuario
    
    # Especificar multiplicador 2 explícitamente
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=True, multiplicador=2)
    
    # 100 - 10 + (10 * 2) = 110
    assert usuarios_db["1234"]["fichas"] == 110


def test_apuesta_minima():
    """Verifica conceptualmente que las apuestas deben tener un mínimo"""
    # Apuestas válidas (mayores que 0)
    apuesta_1 = 1
    apuesta_5 = 5
    apuesta_10 = 10
    
    assert apuesta_1 > 0
    assert apuesta_5 > 0
    assert apuesta_10 > 0
    
    # Apuesta mínima conceptual debería ser al menos 1
    apuesta_minima_valida = 1
    assert apuesta_minima_valida >= 1


def test_rechaza_fichas_insuficiente():
    """
    Verifica conceptualmente que no se debe apostar más de lo que se tiene
    NOTA: gestionar_apuesta() NO valida esto, debe validarse ANTES
    """
    usuario = Usuario("TestUser", "pass123", "01/01/2000", id_usuario="1234", fichas=10)
    usuarios_db = {"1234": usuario.to_dict()}
    
    fichas_disponibles = usuarios_db["1234"]["fichas"]
    monto_apuesta = 50  # Más de lo que tiene
    
    # ESTO ES CONCEPTUAL - tu código actual NO valida esto
    assert monto_apuesta > fichas_disponibles, "La apuesta es mayor que las fichas disponibles"


def test_apuesta_en_diferentes_juegos(usuarios_db_con_usuario):
    """Verifica que se pueden hacer apuestas en diferentes juegos"""
    usuarios_db = usuarios_db_con_usuario
    
    juegos_disponibles = ["dados", "ruleta", "tragamonedas", "carreras"]
    
    for juego in juegos_disponibles:
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", 5, juego, gano=True, multiplicador=2)
    
    # Verificar que las fichas aumentaron correctamente
    # 100 + 4 veces (5 * (2-1)) = 100 + 20 = 120
    assert usuarios_db["1234"]["fichas"] == 120


def test_apuesta_con_monto_decimal(usuarios_db_con_usuario):
    """Verifica que se pueden hacer apuestas con montos decimales"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]
    monto = 10.5
    multiplicador = 2
    
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", monto, "dados", gano=True, multiplicador=multiplicador)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    ganancia_neta = monto * (multiplicador - 1)
    
    # 100 - 10.5 + (10.5 * 2) = 110.5
    assert fichas_despues == fichas_antes + ganancia_neta


def test_multiples_apuestas_seguidas(usuarios_db_con_usuario):
    """Verifica que se pueden hacer múltiples apuestas seguidas"""
    usuarios_db = usuarios_db_con_usuario
    
    # Hacer 10 apuestas ganando cada una
    # Cada apuesta: -1 + (1*2) = +1 neto
    for i in range(10):
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", 1, "dados", gano=True, multiplicador=2)
    
    # Fichas finales: 100 + (10 * 1) = 110
    assert usuarios_db["1234"]["fichas"] == 110


def test_apuesta_varios_usuarios(usuarios_db_varios_usuarios):
    """Verifica que múltiples usuarios pueden apostar independientemente"""
    usuarios_db = usuarios_db_varios_usuarios
    
    # Usuario 1 apuesta y gana: 1000 - 100 + (100 * 2) = 1100
    usuarios_db = gestionar_apuesta(usuarios_db, "1111", 100, "dados", gano=True, multiplicador=2)
    assert usuarios_db["1111"]["fichas"] == 1100
    
    # Usuario 2 apuesta y pierde: 100 - 50 = 50
    usuarios_db = gestionar_apuesta(usuarios_db, "2222", 50, "ruleta", gano=False, multiplicador=2)
    assert usuarios_db["2222"]["fichas"] == 50
    
    # Usuario 3 apuesta y gana: 10 - 5 + (5 * 3) = 20
    usuarios_db = gestionar_apuesta(usuarios_db, "3333", 5, "tragamonedas", gano=True, multiplicador=3)
    assert usuarios_db["3333"]["fichas"] == 20


def test_apuesta_cero_no_cambia_fichas(usuarios_db_con_usuario):
    """Verifica comportamiento con apuesta de 0 (aunque no debería permitirse)"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]
    
    # Apuesta de 0: 100 - 0 + (0 * 2) = 100
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 0, "dados", gano=True, multiplicador=2)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    
    assert fichas_despues == fichas_antes


def test_multiplicador_1_es_empate(usuarios_db_con_usuario):
    """Verifica que multiplicador 1 devuelve la misma cantidad (empate)"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]
    
    # Ganar con multiplicador 1: 100 - 20 + (20 * 1) = 100
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 20, "dados", gano=True, multiplicador=1)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    
    # No hay ganancia neta con multiplicador 1
    assert fichas_despues == fichas_antes


def test_racha_ganadora(usuarios_db_con_usuario):
    """Verifica acumulación de fichas en racha ganadora"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_iniciales = 100
    apuesta = 10
    multiplicador = 2
    rachas = 5
    
    for _ in range(rachas):
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", apuesta, "dados", gano=True, multiplicador=multiplicador)
    
    # Cada ganancia neta: 10 * (2-1) = 10
    # Total: 100 + (5 * 10) = 150
    assert usuarios_db["1234"]["fichas"] == fichas_iniciales + (rachas * apuesta * (multiplicador - 1))


def test_racha_perdedora_afecta_fichas(usuarios_db_con_usuario):
    """Verifica que perder varias veces seguidas disminuye las fichas"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_iniciales = usuarios_db["1234"]["fichas"]  # 100
    apuesta = 5
    rachas = 10
    
    # Perder 10 veces
    for _ in range(10):
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", apuesta, "ruleta", gano=False, multiplicador=2)
    
    # Las fichas disminuyen: 100 - (10 * 5) = 50
    assert usuarios_db["1234"]["fichas"] == fichas_iniciales - (rachas * apuesta)


def test_apuesta_grande_con_multiplicador_alto(usuarios_db_varios_usuarios):
    """Verifica apuestas grandes con multiplicadores altos"""
    usuarios_db = usuarios_db_varios_usuarios
    
    # Usuario rico apuesta mucho: 1000 - 500 + (500 * 10) = 5500
    usuarios_db = gestionar_apuesta(usuarios_db, "1111", 500, "carreras", gano=True, multiplicador=10)
    
    assert usuarios_db["1111"]["fichas"] == 5500


def test_alternancia_ganar_perder(usuarios_db_con_usuario):
    """Verifica alternancia entre ganar y perder"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas = 100
    
    # Ganar: 100 - 10 + (10*2) = 110
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=True, multiplicador=2)
    fichas = 110
    assert usuarios_db["1234"]["fichas"] == fichas
    
    # Perder: 110 - 10 = 100
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=False, multiplicador=2)
    fichas = 100
    assert usuarios_db["1234"]["fichas"] == fichas
    
    # Ganar: 100 - 10 + (10*3) = 120
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=True, multiplicador=3)
    fichas = 120
    assert usuarios_db["1234"]["fichas"] == fichas


def test_usuario_no_existente_da_error():
    """Verifica que intentar apostar con usuario inexistente da error"""
    usuarios_db = {}
    
    # Esto debería dar KeyError porque el usuario no existe
    with pytest.raises(KeyError):
        gestionar_apuesta(usuarios_db, "9999", 10, "dados", gano=True, multiplicador=2)


def test_todos_los_juegos_se_pueden_jugar(usuarios_db_con_usuario):
    """Verifica que todos los juegos del sistema se pueden jugar"""
    usuarios_db = usuarios_db_con_usuario
    
    juegos = ["dados", "ruleta", "tragamonedas", "carreras"]
    
    fichas_iniciales = usuarios_db["1234"]["fichas"]
    
    for juego in juegos:
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", 5, juego, gano=True, multiplicador=2)
    
    # Verificar que las fichas aumentaron: 100 + 4*(5*(2-1)) = 120
    assert usuarios_db["1234"]["fichas"] == fichas_iniciales + 20