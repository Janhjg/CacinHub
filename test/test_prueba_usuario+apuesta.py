import pytest
import os
import json
import sys

"""Añade la raíz al path para que encuentre 'funciones.py'"""
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from funciones import crear_usuario, gestionar_apuesta

"""Ajusta la ruta para que apunte a la carpeta de base de datos"""
DB_TEST = os.path.join("user_test.json")

def test_1_creacion_y_archivo():
    """Verifica la creación del usuario Zack y escritura en JSON."""
    """Asegura que la carpeta exista"""
    os.makedirs("base_de_datos", exist_ok=True)
    
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
    """Comprueba que Zack inicie con 100 fichas"""
    with open(DB_TEST, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    uid = list(datos.keys())[0]
    assert datos[uid]["fichas"] == 100

def test_3_gestion_apuesta_tamamo_cross():
    """Apuesta 50 fichas por Tamamo Cross (x3) y valida las fichas"""
    with open(DB_TEST, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    uid = list(datos.keys())[0]
    fichas_antes = datos[uid]["fichas"]
    
    apuesta = 50
    datos[uid]["fichas"] -= apuesta
    
    """Simulamos victoria de Tamamo Cross (multiplicador 3)
    Resultado esperado: 50 + (50 * 3) = 200"""
    db_final = gestionar_apuesta(datos, uid, apuesta, "carreras", True, 3)
    fichas_despues = db_final[uid]["fichas"]
    
    with open(DB_TEST, "w", encoding="utf-8") as f:
        json.dump(db_final, f, indent=4)
    
    assert fichas_despues == 200
    assert fichas_despues != fichas_antes
    assert db_final[uid]["stats"]["carreras"] == 1