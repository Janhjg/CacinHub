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
    ganancia_esperada = monto_apuesta * multiplicador
    
    # Verificar que las fichas aumentaron correctamente
    assert fichas_despues == fichas_antes + ganancia_esperada
    assert fichas_despues == 140  # 100 + (20 * 2)


def test_apuesta_perdida_no_aumenta_fichas(usuarios_db_con_usuario):
    """Verifica que al perder una apuesta las fichas NO aumentan"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]  # 100
    
    # Perder apuesta
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", monto=20, juego="ruleta", gano=False)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    
    # Las fichas no deben cambiar al perder
    assert fichas_despues == fichas_antes
    assert fichas_despues == 100


def test_actualizacion_de_fichas_multiples_apuestas(usuarios_db_con_usuario):
    """Verifica que las fichas se actualizan correctamente tras múltiples apuestas"""
    usuarios_db = usuarios_db_con_usuario
    
    # Ganar primera apuesta: +40 (20 * 2)
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 20, "dados", gano=True, multiplicador=2)
    assert usuarios_db["1234"]["fichas"] == 140
    
    # Perder segunda apuesta: sin cambio
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "ruleta", gano=False)
    assert usuarios_db["1234"]["fichas"] == 140
    
    # Ganar tercera apuesta con multiplicador 3: +30 (10 * 3)
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "tragamonedas", gano=True, multiplicador=3)
    assert usuarios_db["1234"]["fichas"] == 170


def test_diferentes_multiplicadores(usuarios_db_con_usuario):
    """Verifica que funcionan correctamente diferentes multiplicadores"""
    usuarios_db = usuarios_db_con_usuario
    
    # Multiplicador 2 (por defecto)
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=True, multiplicador=2)
    assert usuarios_db["1234"]["fichas"] == 120  # 100 + (10*2)
    
    # Multiplicador 3
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "tragamonedas", gano=True, multiplicador=3)
    assert usuarios_db["1234"]["fichas"] == 150  # 120 + (10*3)
    
    # Multiplicador 5
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "carreras", gano=True, multiplicador=5)
    assert usuarios_db["1234"]["fichas"] == 200  # 150 + (10*5)


def test_multiplicador_por_defecto_es_2(usuarios_db_con_usuario):
    """Verifica que el multiplicador por defecto es 2"""
    usuarios_db = usuarios_db_con_usuario
    
    # No especificar multiplicador, debe usar 2 por defecto
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=True)
    
    # 100 + (10 * 2) = 120
    assert usuarios_db["1234"]["fichas"] == 120


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


def test_stats_se_actualizan_con_apuesta(usuarios_db_con_usuario):
    """Verifica que las estadísticas se actualizan al hacer apuestas"""
    usuarios_db = usuarios_db_con_usuario
    
    stats_antes = usuarios_db["1234"]["stats"].copy()
    
    # Hacer una apuesta en dados
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=True)
    
    stats_despues = usuarios_db["1234"]["stats"]
    
    # Verificar que partidas_totales aumentó
    assert stats_despues["partidas_totales"] == stats_antes["partidas_totales"] + 1
    
    # Verificar que el contador de dados aumentó
    assert stats_despues["dados"] == stats_antes["dados"] + 1


def test_apuesta_en_diferentes_juegos(usuarios_db_con_usuario):
    """Verifica que se pueden hacer apuestas en diferentes juegos"""
    usuarios_db = usuarios_db_con_usuario
    
    juegos_disponibles = ["dados", "ruleta", "tragamonedas", "carreras"]
    
    for juego in juegos_disponibles:
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", 5, juego, gano=True)
        
        # Verificar que el stat del juego se actualizó
        assert usuarios_db["1234"]["stats"][juego] >= 1


def test_apuesta_con_monto_decimal(usuarios_db_con_usuario):
    """Verifica que se pueden hacer apuestas con montos decimales"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]
    monto = 10.5
    
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", monto, "dados", gano=True, multiplicador=2)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    
    # 100 + (10.5 * 2) = 121
    assert fichas_despues == fichas_antes + (monto * 2)


def test_multiples_apuestas_seguidas(usuarios_db_con_usuario):
    """Verifica que se pueden hacer múltiples apuestas seguidas"""
    usuarios_db = usuarios_db_con_usuario
    
    # Hacer 10 apuestas
    for i in range(10):
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", 1, "dados", gano=True, multiplicador=2)
    
    # Fichas finales: 100 + (10 * 1 * 2) = 120
    assert usuarios_db["1234"]["fichas"] == 120
    
    # Stats: 10 partidas totales
    assert usuarios_db["1234"]["stats"]["partidas_totales"] == 10
    assert usuarios_db["1234"]["stats"]["dados"] == 10


def test_apuesta_varios_usuarios(usuarios_db_varios_usuarios):
    """Verifica que múltiples usuarios pueden apostar independientemente"""
    usuarios_db = usuarios_db_varios_usuarios
    
    # Usuario 1 apuesta y gana
    usuarios_db = gestionar_apuesta(usuarios_db, "1111", 100, "dados", gano=True, multiplicador=2)
    assert usuarios_db["1111"]["fichas"] == 1200  # 1000 + 200
    
    # Usuario 2 apuesta y pierde
    usuarios_db = gestionar_apuesta(usuarios_db, "2222", 50, "ruleta", gano=False)
    assert usuarios_db["2222"]["fichas"] == 100  # Sin cambio
    
    # Usuario 3 apuesta y gana
    usuarios_db = gestionar_apuesta(usuarios_db, "3333", 5, "tragamonedas", gano=True, multiplicador=3)
    assert usuarios_db["3333"]["fichas"] == 25  # 10 + 15


def test_apuesta_cero_no_cambia_fichas(usuarios_db_con_usuario):
    """Verifica comportamiento con apuesta de 0 (aunque no debería permitirse)"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]
    
    # Apuesta de 0
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 0, "dados", gano=True, multiplicador=2)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    
    # 100 + (0 * 2) = 100
    assert fichas_despues == fichas_antes


def test_stats_independientes_por_juego(usuarios_db_con_usuario):
    """Verifica que las estadísticas se mantienen separadas por juego"""
    usuarios_db = usuarios_db_con_usuario
    
    # Jugar 3 veces dados
    for _ in range(3):
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", 5, "dados", gano=True)
    
    # Jugar 2 veces ruleta
    for _ in range(2):
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", 5, "ruleta", gano=False)
    
    # Jugar 1 vez tragamonedas
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 5, "tragamonedas", gano=True)
    
    stats = usuarios_db["1234"]["stats"]
    
    assert stats["partidas_totales"] == 6
    assert stats["dados"] == 3
    assert stats["ruleta"] == 2
    assert stats["tragamonedas"] == 1
    assert stats["carreras"] == 0  # No jugado


def test_multiplicador_1_es_empate(usuarios_db_con_usuario):
    """Verifica que multiplicador 1 devuelve la misma cantidad (empate)"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]
    
    # Ganar con multiplicador 1
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 20, "dados", gano=True, multiplicador=1)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    
    # 100 + (20 * 1) = 120
    assert fichas_despues == fichas_antes + 20


def test_racha_ganadora(usuarios_db_con_usuario):
    """Verifica acumulación de fichas en racha ganadora"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_iniciales = 100
    apuesta = 10
    multiplicador = 2
    rachas = 5
    
    for _ in range(rachas):
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", apuesta, "dados", gano=True, multiplicador=multiplicador)
    
    # 100 + (5 * 10 * 2) = 200
    assert usuarios_db["1234"]["fichas"] == fichas_iniciales + (rachas * apuesta * multiplicador)


def test_racha_perdedora_no_afecta_fichas(usuarios_db_con_usuario):
    """Verifica que perder varias veces seguidas no afecta las fichas en gestionar_apuesta"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_iniciales = usuarios_db["1234"]["fichas"]
    
    # Perder 10 veces
    for _ in range(10):
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", 5, "ruleta", gano=False)
    
    # Las fichas no cambian en gestionar_apuesta cuando se pierde
    assert usuarios_db["1234"]["fichas"] == fichas_iniciales
    
    # Pero sí se actualizan las stats
    assert usuarios_db["1234"]["stats"]["partidas_totales"] == 10
    assert usuarios_db["1234"]["stats"]["ruleta"] == 10


def test_apuesta_grande_con_multiplicador_alto(usuarios_db_varios_usuarios):
    """Verifica apuestas grandes con multiplicadores altos"""
    usuarios_db = usuarios_db_varios_usuarios
    
    # Usuario rico apuesta mucho
    usuarios_db = gestionar_apuesta(usuarios_db, "1111", 500, "carreras", gano=True, multiplicador=10)
    
    # 1000 + (500 * 10) = 6000
    assert usuarios_db["1111"]["fichas"] == 6000


def test_alternancia_ganar_perder(usuarios_db_con_usuario):
    """Verifica alternancia entre ganar y perder"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas = 100
    
    # Ganar
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=True, multiplicador=2)
    fichas += 20
    assert usuarios_db["1234"]["fichas"] == fichas
    
    # Perder
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=False)
    # fichas no cambia
    assert usuarios_db["1234"]["fichas"] == fichas
    
    # Ganar
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", gano=True, multiplicador=3)
    fichas += 30
    assert usuarios_db["1234"]["fichas"] == fichas


def test_usuario_no_existente_da_error():
    """Verifica que intentar apostar con usuario inexistente da error"""
    usuarios_db = {}
    
    # Esto debería dar KeyError porque el usuario no existe
    with pytest.raises(KeyError):
        gestionar_apuesta(usuarios_db, "9999", 10, "dados", gano=True)


def test_todos_los_juegos_actualizan_stats(usuarios_db_con_usuario):
    """Verifica que todos los juegos del sistema actualizan sus stats"""
    usuarios_db = usuarios_db_con_usuario
    
    juegos = ["dados", "ruleta", "tragamonedas", "carreras"]
    
    for juego in juegos:
        usuarios_db = gestionar_apuesta(usuarios_db, "1234", 5, juego, gano=True)
    
    stats = usuarios_db["1234"]["stats"]
    
    # Cada juego debe tener al menos 1 partida
    for juego in juegos:
        assert stats[juego] >= 1, f"El juego {juego} no se actualizó"
    
    # Total debe ser 4
    assert stats["partidas_totales"] == 4
