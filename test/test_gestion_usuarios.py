from funciones import *
import pytest
def test_creacion_usuario():
    data = "./base_data./users.json"
    try:
        with open(data, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data["id"] != None and data["saldo"] >= 100:
                return "Existe"
            else:
                return None
    except ValueError:
        return cargar_datos()


print(test_creacion_usuario())
def test_nombres_no_duplicados():
    pass

def test_saldo_minimo():
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
        assert "saldo" in resultado
        assert "fecha_registro" in resultado
        assert "total_partidas" in resultado
        assert "partidas_por_juego" in resultado
        
        # 4. Verificar que los datos son correctos
        assert resultado["nombre"] == "TestUser"
        assert resultado["saldo"] == 100
        
    def test_consultar_usuario_inexistente():
    
     # 1. Intentar consultar un ID que no existe
     user_id = "id_falso_9999"
    
     # 2. Verificar que da error
     with pytest.raises(Exception):
         consultar_usuario(user_id)
    

