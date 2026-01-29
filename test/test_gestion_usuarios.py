from funciones import *
import pytest
import json

# ----------------------
# TEST CREACION USUARIO
# ----------------------

def test_creacion_usuario():
    # comprueba que se cree bien
    data = "users.json"
    try:
        with open(data, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data["id"] != None and data["fichas"] >= 100:
                return "Existe"
            else:
                return None
    except ValueError:
        return cargar_datos()

def test_nombres_no_duplicados():
    pass

def test_fichas_minimas():
    pass

# ----------------------
# TEST CONSULTAR USUARIO
# ----------------------

def test_consultar_usuario():
    
    def test_consultar_usuario_existente():
        # 1. Crear un usuario de prueba
        usuario = crear_usuario("TestUser", "pass123", 100)
        user_id = usuario["id"]
        
        # 2. Consultar el usuario
        resultado = consultar_usuario(user_id)
        
        # 3. Verificar que tiene todos los campos
        assert "id" in resultado
        assert "nombre" in resultado
        assert "contraseña" in resultado
        assert "fichas" in resultado
        assert "fecha_registro" in resultado
        assert "total_partidas" in resultado
        assert "partidas_por_juego" in resultado
        
        # 4. Verificar que los datos son correctos
        assert resultado["nombre"] == "TestUser"
        assert resultado["fichas"] == 100
        
    def test_consultar_usuario_inexistente():
    
     # 1. Intentar consultar un ID que no existe
     user_id = "id_falso_9999"
    
     # 2. Verificar que da error
     with pytest.raises(Exception):
         consultar_usuario(user_id)
    
# ----------------------------
# Tests de fichas
# ----------------------------

# Las fichas iniciales del usuario debe ser exactamente 100 fichas
def test_fichas_iniciales_correcto():

    usuarios = consultar_usuarios()
    usuario = usuarios[0]

    assert usuario["fichas"] == fichas_iniciales, (
        f"Las fichas iniciales deben ser {fichas_iniciales}"
    )

# Comprueba que un depósito positivo incrementa de fichas
def test_fichas_incrementado():

    usuarios = consultar_usuarios()
    usuario = usuarios[0]

    fichas_iniciales = usuario["fichas"]
    deposito = 50.0

    fichas_finales = fichas_inicial + deposito

    assert fichas_finales > fichas_iniciales
    assert fichas_finales == fichas_iniciales + deposito

# No se debe permitir un depósito de 0
def test_rechazo_deposito_cero():

        deposito = 0.0

        assert deposito > 0, "No se debe permitir un depósito de 0"

# No se permiten valores negativos ni en fichas ni en depósitos
def test_no_numeros_negativos():

    usuarios = cargar_usuarios()
    usuario = usuarios[0]

    fichas = usuario["fichas"]
    deposito = -10.0

    assert fichas > 0, "Las fichas no puede ser negativo"
    assert deposito > 0, "No se permiten depósitos negativos"
