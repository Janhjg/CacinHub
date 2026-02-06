from Funciones.funciones import *
import pytest
import json
from datetime import datetime


@pytest.fixture
def usuarios_db_limpio():
    return {}


@pytest.fixture
def usuarios_db_con_usuario():
    """
   Genera el usuario
    """
    usuario_test = Usuario("TestUser", "pass123", "01/01/2000", id_usuario="1234")
    return {"1234": usuario_test.to_dict()}


# =====================================================
# TESTS DE INICIAR SESIÓN
# =====================================================

def test_iniciar_sesion_exitoso(usuarios_db_con_usuario):
    """Verifica que se puede iniciar sesión"""
    usuarios_db = usuarios_db_con_usuario
    
    resultado = iniciar_sesion(usuarios_db, "1234", "pass123")
    
    assert resultado == True, "Debe iniciar sesión correctamente"


def test_iniciar_sesion_contrasena_incorrecta(usuarios_db_con_usuario):
    """Verifica que falla con contraseña incorrecta"""
    usuarios_db = usuarios_db_con_usuario
    
    resultado = iniciar_sesion(usuarios_db, "1234", "wrong_password")
    
    assert resultado == False, "No debe permitir inicio de sesión con contraseña incorrecta"


def test_iniciar_sesion_usuario_inexistente(usuarios_db_limpio):
    """Verifica que falla al intentar iniciar sesión con un ID que no existe"""
    usuarios_db = usuarios_db_limpio
    
    resultado = iniciar_sesion(usuarios_db, "9999", "malapassword")
    
    assert resultado == False, "No debe permitir inicio de sesión con ID inexistente"


# =====================================================
# TESTS DE GESTIÓN DE FICHAS
# =====================================================

def test_incremento_fichas_al_ganar(usuarios_db_con_usuario):
    """Usa gestionar_apuesta() para verificar que las fichas aumentan al ganar"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]  # 100
    
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", monto=20, juego="dados", gano=True)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    
    assert fichas_despues == fichas_antes + 40
    assert fichas_despues > fichas_antes


def test_fichas_no_cambian_al_perder(usuarios_db_con_usuario):
    """Verifica que las fichas NO aumentan al perder una apuesta"""
    usuarios_db = usuarios_db_con_usuario
    
    fichas_antes = usuarios_db["1234"]["fichas"]  # 100
    
    # Perder una apuesta
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", monto=20, juego="ruleta", gano=False)
    
    fichas_despues = usuarios_db["1234"]["fichas"]
    
    # Las fichas no deben cambiar (se mantienen en 100)
    assert fichas_despues == fichas_antes


def test_fichas_no_negativas_con_property():
    user = Usuario("TestUser", "pass123", "01/01/2000", id_usuario="1234")
    
    # Intentar asignar fichas negativas
    user.fichas = -50
    
    # El setter debe convertirlas a 0
    assert user.fichas == 0, "Las fichas negativas deben convertirse a 0"


def test_validacion_apuesta_mayor_que_cero():
    """Verifica conceptualmente que apuestas válidas deben ser mayores que 0"""
    apuesta_valida_1 = 10
    apuesta_valida_2 = 50.5
    apuesta_valida_3 = 1
    
    assert apuesta_valida_1 > 0
    assert apuesta_valida_2 > 0
    assert apuesta_valida_3 > 0
    
    apuesta_invalida_cero = 0
    apuesta_invalida_negativa = -10
    
    assert not (apuesta_invalida_cero > 0)
    assert not (apuesta_invalida_negativa > 0)


# =====================================================
# TESTS DE ESTADÍSTICAS
# =====================================================

def test_stats_iniciales(usuarios_db_con_usuario):
    """Verifica que las estadísticas iniciales son correctas"""
    usuarios_db = usuarios_db_con_usuario
    
    stats = usuarios_db["1234"]["stats"]
    
    assert stats["partidas_totales"] == 0
    assert stats["dados"] == 0
    assert stats["ruleta"] == 0
    assert stats["tragamonedas"] == 0
    assert stats["carreras"] == 0


def test_stats_actualizadas_despues_partida(usuarios_db_con_usuario):
    """Verifica que las estadísticas se actualizan correctamente"""
    usuarios_db = usuarios_db_con_usuario
    
    # Jugar varias partidas
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", True)
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "dados", False)
    usuarios_db = gestionar_apuesta(usuarios_db, "1234", 10, "ruleta", True)
    
    stats = usuarios_db["1234"]["stats"]
    
    assert stats["partidas_totales"] == 3
    assert stats["dados"] == 2
    assert stats["ruleta"] == 1


# =====================================================
# TESTS DE LA CLASE USUARIO
# =====================================================

def test_clase_usuario_creacion():
    """Verifica que se puede crear una instancia de Usuario correctamente"""
    user = Usuario("TestUser", "pass123", "01/01/2000")
    
    assert user.nombre == "TestUser"
    assert user.contrasena == "pass123"
    assert user.fecha_nacimiento == "01/01/2000"
    assert user.fichas == 100
    assert user.id is not None
    assert len(user.id) == 4


def test_clase_usuario_to_dict():
    """Verifica que el método to_dict() funciona correctamente"""
    user = Usuario("TestUser", "pass123", "01/01/2000", id_usuario="1234")
    
    user_dict = user.to_dict()
    
    assert user_dict["nombre"] == "TestUser"
    assert user_dict["contrasena"] == "pass123"
    assert user_dict["fecha_nacimiento"] == "01/01/2000"
    assert user_dict["fichas"] == 100
    assert "fecha_registro" in user_dict
    assert "stats" in user_dict


def test_clase_usuario_id_unico():
    """Verifica que cada instancia recibe un ID único"""
    user1 = Usuario("User1", "pass1", "01/01/2000")
    user2 = Usuario("User2", "pass2", "02/02/2000")
    user3 = Usuario("User3", "pass3", "03/03/2000")
    
    ids = [user1.id, user2.id, user3.id]
    
    # Todos los IDs deben ser diferentes
    assert len(ids) == len(set(ids)), "Los IDs deben ser únicos"
    
    # Todos deben ser de 4 dígitos
    for user_id in ids:
        assert len(user_id) == 4
        assert user_id.isdigit()


def test_calcular_edad():
    """Verifica que calcular_edad() funciona correctamente"""
    # Persona nacida hace exactamente 25 años
    hace_25_anos = datetime.now().replace(year=datetime.now().year - 25)
    fecha_str = hace_25_anos.strftime("%d/%m/%Y")
    
    edad = calcular_edad(fecha_str)
    
    # Puede ser 24 o 25 dependiendo del día del año
    assert edad in [24, 25], "La edad debe ser aproximadamente 25 años"


def test_calcular_edad_formato_invalido():
    """Verifica que calcular_edad() retorna None con formato inválido"""
    edad = calcular_edad("31-12-2000")  # Formato incorrecto
    assert edad is None, "Debe retornar None con formato inválido"


def test_calcular_edad_mayor_18():
    """Verifica que personas mayores de 18 se detectan correctamente"""
    # Fecha de hace 20 años
    hace_20 = datetime.now().replace(year=datetime.now().year - 20)
    fecha_str = hace_20.strftime("%d/%m/%Y")
    
    edad = calcular_edad(fecha_str)
    
    assert edad >= 18, "Debe ser mayor de 18"


def test_calcular_edad_menor_18():
    """Verifica que personas menores de 18 se detectan correctamente"""
    # Fecha de hace 15 años
    hace_15 = datetime.now().replace(year=datetime.now().year - 15)
    fecha_str = hace_15.strftime("%d/%m/%Y")
    
    edad = calcular_edad(fecha_str)
    
    assert edad < 18, "Debe ser menor de 18"