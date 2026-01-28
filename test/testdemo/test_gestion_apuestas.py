from funciones import *
import pytest
import json
data = "users.json"
historial = "historial.json"
def test_verificar_apuesta():
    payload = data["id", "fichas"]
    juego = juegos["ruleta"]
        
    assert "resultado" in historial
    assert historial["resultado"] in ["gano", "perdio"]
    assert "ganancia" in data
    assert isinstance(data["ganancia"], (int, float))
            


def test_actualizacion_de_fichas():
    pass

def test_rechaza_fichas_insuficiente():
    pass

def test_apuesta_minima():
    pass

