from funciones import *
import pytest
import json
data = "./base_data./users.json"
def test_verificar_apuesta():
    try: 
        with open(data, "r", encoding="utf-8") as f:
            data = json.load(f)
            apuesta = None
            if data["saldo"] 


def test_actualizacion_de_saldo():
    pass

def test_rechaza_saldo_insuficiente():
    pass

def test_apuesta_minima():
    pass

