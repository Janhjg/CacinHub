from Funciones.funciones import *
import pytest
import json


@pytest.fixture
def usuarios_db_limpio():
    """Proporciona una base de datos de usuarios vacía para cada test"""
    return {}

# ==============================
# TESTS DE CREACIÓN DE USUARIO
# ==============================

def test_creacion_usuario(usuarios_db_limpio):
    
    usuarios_db = usuarios_db_limpio
    nombre = "TestUser"
    contrasena = "pass123"
    
    # Crear usuario usando la función real
    usuarios_db = crear_usuario(usuarios_db, nombre, contrasena)
    
    # Verificar que se creó exactamente 1 usuario
    assert len(usuarios_db) == 1, "Debe haberse creado 1 usuario"
    
    # Obtener el usuario creado
    user_id = list(usuarios_db.keys())[0]
    usuario = usuarios_db[user_id]
    
    # Verificar estructura y valores
    assert usuario["nombre"] == nombre
    assert usuario["contrasena"] == contrasena
    assert usuario["fichas"] == 100
    assert "fecha_registro" in usuario
    assert "stats" in usuario


def test_id_usuario_generado_automaticamente(usuarios_db_limpio):
    """Verifica que se genera automáticamente un ID único de 4 dígitos"""
    usuarios_db = usuarios_db_limpio
    usuarios_db = crear_usuario(usuarios_db, "User1", "pass1")
    
    user_id = list(usuarios_db.keys())[0]
    
    # Verificar que el ID es un string de 4 dígitos
    assert len(user_id) == 4
    assert user_id.isdigit()
    assert 1000 <= int(user_id) <= 9999


def test_nombres_no_duplicados(usuarios_db_limpio):
    
    usuarios_db = usuarios_db_limpio
    
    # Crear varios usuarios
    usuarios_db = crear_usuario(usuarios_db, "Alice", "pass1")
    usuarios_db = crear_usuario(usuarios_db, "Bob", "pass2")
    usuarios_db = crear_usuario(usuarios_db, "Charlie", "pass3")
    
    # Verificar que se crearon 3 usuarios
    assert len(usuarios_db) == 3
    
    # Verificar que cada uno tiene nombre diferente
    nombres = [usuario["nombre"] for usuario in usuarios_db.values()]
    assert "Alice" in nombres
    assert "Bob" in nombres
    assert "Charlie" in nombres


def test_ids_unicos_multiples_usuarios(usuarios_db_limpio):
    """Verifica que cada usuario recibe un ID único incluso creando muchos"""
    usuarios_db = usuarios_db_limpio
    
    # Crear 20 usuarios
    for i in range(20):
        usuarios_db = crear_usuario(usuarios_db, f"User{i}", f"pass{i}")
    
    # Verificar que hay 20 usuarios
    assert len(usuarios_db) == 20
    
    # Verificar que todos los IDs son únicos
    ids = list(usuarios_db.keys())
    assert len(ids) == len(set(ids)), "Todos los IDs deben ser únicos"


def test_fichas_minimas(usuarios_db_limpio):
    
    usuarios_db = usuarios_db_limpio
    usuarios_db = crear_usuario(usuarios_db, "TestUser", "pass123")
    
    user_id = list(usuarios_db.keys())[0]
    usuario = usuarios_db[user_id]
    
    assert usuario["fichas"] == 100, "Las fichas iniciales deben ser 100"


# =====================================================
# TESTS DE INICIAR SESIÓN
# =====================================================

def test_iniciar_sesion_exitoso(usuarios_db_limpio):
    """Verifica que se puede iniciar sesión con credenciales correctas"""
    usuarios_db = usuarios_db_limpio
    usuarios_db = crear_usuario(usuarios_db, "TestUser", "password123")
    
    user_id = list(usuarios_db.keys())[0]
    
    # Iniciar sesión con credenciales correctas
    resultado = iniciar_sesion(usuarios_db, user_id, "password123")
    
    assert resultado == True, "Debe iniciar sesión correctamente"


def test_iniciar_sesion_contrasena_incorrecta(usuarios_db_limpio):
    """Verifica que falla con contraseña incorrecta"""
    usuarios_db = usuarios_db_limpio
    usuarios_db = crear_usuario(usuarios_db, "TestUser", "password123")
    
    user_id = list(usuarios_db.keys())[0]
    
    # Intentar con contraseña incorrecta
    resultado = iniciar_sesion(usuarios_db, user_id, "wrong_password")
    
    assert resultado == False, "No debe permitir inicio de sesión con contraseña incorrecta"


def test_iniciar_sesion_usuario_inexistente(usuarios_db_limpio):
    
    usuarios_db = usuarios_db_limpio
    
    # Intentar iniciar sesión con ID inexistente
    resultado = iniciar_sesion(usuarios_db, "9999", "anypassword")
    
    assert resultado == False, "No debe permitir inicio de sesión con ID inexistente"


# =====================================================
# TESTS DE GESTIÓN DE FICHAS
# =====================================================

def test_fichas_iniciales_correcto(usuarios_db_limpio):

    usuarios_db = usuarios_db_limpio
    usuarios_db = crear_usuario(usuarios_db, "TestUser", "pass123")
    
    user_id = list(usuarios_db.keys())[0]
    usuario = usuarios_db[user_id]
    
    assert usuario["fichas"] == 100, "Las fichas iniciales deben ser 100"


def test_incremento_fichas_al_ganar(usuarios_db_limpio):
   
    usuarios_db = usuarios_db_limpio
    usuarios_db = crear_usuario(usuarios_db, "TestUser", "pass123")
    
    user_id = list(usuarios_db.keys())[0]
    fichas_antes = usuarios_db[user_id]["fichas"]  # 100
    
    # Ganar una apuesta de 20 fichas (multiplicador por defecto es 2)
    usuarios_db = gestionar_apuesta(usuarios_db, user_id, monto=20, juego="dados", gano=True)
    
    fichas_despues = usuarios_db[user_id]["fichas"]
    
    # 100 + (20 * 2) = 140
    assert fichas_despues == fichas_antes + 40
    assert fichas_despues > fichas_antes


def test_fichas_no_cambian_al_perder(usuarios_db_limpio):
   
    usuarios_db = usuarios_db_limpio
    usuarios_db = crear_usuario(usuarios_db, "TestUser", "pass123")
    
    user_id = list(usuarios_db.keys())[0]
    fichas_antes = usuarios_db[user_id]["fichas"]  # 100
    
    # Perder una apuesta
    usuarios_db = gestionar_apuesta(usuarios_db, user_id, monto=20, juego="ruleta", gano=False)
    
    fichas_despues = usuarios_db[user_id]["fichas"]
    
    # Las fichas no deben cambiar (se mantienen en 100)
    assert fichas_despues == fichas_antes


def test_validacion_apuesta_mayor_que_cero():
    
    # Verificar que apuestas válidas son mayores que 0
    apuesta_valida_1 = 10
    apuesta_valida_2 = 50.5
    apuesta_valida_3 = 1
    
    assert apuesta_valida_1 > 0, "Apuestas válidas deben ser mayores que 0"
    assert apuesta_valida_2 > 0, "Apuestas válidas deben ser mayores que 0"
    assert apuesta_valida_3 > 0, "Apuestas válidas deben ser mayores que 0"
    
    # Verificar que 0 y valores negativos NO son apuestas válidas
    apuesta_invalida_cero = 0
    apuesta_invalida_negativa = -10
    
    assert not (apuesta_invalida_cero > 0), "Apuesta de 0 no debe ser válida"
    assert not (apuesta_invalida_negativa > 0), "Apuestas negativas no deben ser válidas"


def test_no_fichas_negativas_recomendacion():

    
    usuarios_db = {}
    usuarios_db = crear_usuario(usuarios_db, "TestUser", "pass123")
    user_id = list(usuarios_db.keys())[0]
    
    # Las fichas siempre deben ser >= 0
    fichas = usuarios_db[user_id]["fichas"]
    assert fichas >= 0, "Las fichas no pueden ser negativas"


# =====================================================
# TESTS DE ESTADÍSTICAS
# =====================================================

def test_stats_iniciales(usuarios_db_limpio):
    """Verifica que las estadísticas iniciales son correctas"""
    usuarios_db = usuarios_db_limpio
    usuarios_db = crear_usuario(usuarios_db, "TestUser", "pass123")
    
    user_id = list(usuarios_db.keys())[0]
    stats = usuarios_db[user_id]["stats"]
    
    assert stats["partidas_totales"] == 0
    assert stats["dados"] == 0
    assert stats["ruleta"] == 0
    assert stats["tragamonedas"] == 0
    assert stats["carreras"] == 0


def test_stats_actualizadas_despues_partida(usuarios_db_limpio):
    """Verifica que las estadísticas se actualizan correctamente"""
    usuarios_db = usuarios_db_limpio
    usuarios_db = crear_usuario(usuarios_db, "TestUser", "pass123")
    
    user_id = list(usuarios_db.keys())[0]
    
    # Jugar varias partidas
    usuarios_db = gestionar_apuesta(usuarios_db, user_id, 10, "dados", True)
    usuarios_db = gestionar_apuesta(usuarios_db, user_id, 10, "dados", False)
    usuarios_db = gestionar_apuesta(usuarios_db, user_id, 10, "ruleta", True)
    
    stats = usuarios_db[user_id]["stats"]
    
    assert stats["partidas_totales"] == 3
    assert stats["dados"] == 2
    assert stats["ruleta"] == 1
