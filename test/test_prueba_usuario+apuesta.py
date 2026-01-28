import pytest
import os
import json
from funciones import crear_usuario, gestionar_apuesta

DB_TEST = "user_test.json"

def test_1_creacion_y_archivo():
    """Verifica la creación del usuario Zack y escritura en JSON."""
    db_memoria = {}
    db_memoria = crear_usuario(db_memoria, "Zack", "Zeta123")
    
    with open(DB_TEST, "w", encoding="utf-8") as f:
        json.dump(db_memoria, f, indent=4)
    
    assert os.path.exists(DB_TEST)
    
    with open(DB_TEST, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    uid = list(datos.keys())[0]
    assert datos[uid]["nombre"] == "Zack"

def test_2_verificar_fichas_iniciales():
    """Comprueba que el usuario tiene 100 fichas"""
    with open(DB_TEST, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    uid = list(datos.keys())[0]
    assert datos[uid]["fichas"] == 100

def test_3_gestion_apuesta_de_caballo_numero_2():
    """Crea la apuesta de 50 fichas al 2º caballo, que de un multiplicador de x3 a la apuesta"""
    with open(DB_TEST, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    uid = list(datos.keys())[0]
    fichas_antes = datos[uid]["fichas"]
    
    apuesta = 50
    datos[uid]["fichas"] -= apuesta
    
    db_final = gestionar_apuesta(datos, uid, apuesta, "carreras", True, 3)
    fichas_despues = db_final[uid]["fichas"]
    
    with open(DB_TEST, "w", encoding="utf-8") as f:
        json.dump(db_final, f, indent=4)
    
    assert fichas_despues == 200
    assert fichas_despues != fichas_antes

def test_4_verificar_estadisticas_partidas():
    """Comprueba que el jugador tiene 1 partida en carreras y 1 en total"""
    with open(DB_TEST, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    uid = list(datos.keys())[0]
    stats = datos[uid]["stats"]
    
    assert stats["carreras"] == 1
    assert stats["partidas_totales"] == 1
    assert stats["dados"] == 0

"""def test_5_elimina_archivo_test():

    if os.path.exists(DB_TEST):
        os.remove(DB_TEST)
    
    assert not os.path.exists(DB_TEST)"""