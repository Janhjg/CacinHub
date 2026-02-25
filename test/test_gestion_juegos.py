import json
import pytest
from juegos.base_juegos import Juego
from Funciones.funciones import gestionar_apuesta

# ══════════════════════════════════════════════════════════════
# DATOS FALSOS (reemplazan games.json)
# ══════════════════════════════════════════════════════════════

JUEGOS_FALSOS = [
    {
        "id": "dados",
        "nombre": "Juego de Dados",
        "descripcion": "Lanza los dados y apuesta al resultado.",
        "apuesta_minima": 10,
        "reglas": {
            "opciones": [
                {"tipo": "par",   "valores": [2, 4, 6], "pago": 2},
                {"tipo": "impar", "valores": [1, 3, 5], "pago": 2}
            ]
        }
    },
    {
        "id": "ruleta",
        "nombre": "Ruleta",
        "descripcion": "Apuesta al número o color en la ruleta.",
        "apuesta_minima": 5,
        "reglas": {
            "opciones": [
                {"tipo": "pleno", "valores": [0, 1, 2], "pago": 35},
                {"tipo": "rojo",  "valores": ["rojo"],  "pago": 2},
                {"tipo": "negro", "valores": ["negro"], "pago": 2}
            ]
        }
    },
    {
        "id": "tragamonedas",
        "nombre": "Tragamonedas",
        "descripcion": "Prueba tu suerte con la máquina tragamonedas.",
        "apuesta_minima": 10,
        "reglas": {
            "opciones": [
                {"tipo": "jackpot", "valores": ["🍒🍒🍒"], "pago": 10},
                {"tipo": "par",     "valores": ["dos_iguales"], "pago": 2}
            ]
        }
    },
    {
        "id": "carreras",
        "nombre": "Carreras de Caballos",
        "descripcion": "Apuesta a tu caballo favorito y gana si llega primero.",
        "apuesta_minima": 10,
        "reglas": {
            "opciones": [
                {"tipo": "caballo_1", "valores": ["1"], "pago": 3},
                {"tipo": "caballo_2", "valores": ["2"], "pago": 3},
                {"tipo": "caballo_3", "valores": ["3"], "pago": 3},
                {"tipo": "caballo_4", "valores": ["4"], "pago": 3}
            ]
        }
    }
]

# ══════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════

@pytest.fixture()
def juegos(monkeypatch):
    """Devuelve los juegos falsos sin leer ningún archivo."""
    monkeypatch.setattr("builtins.open", lambda *a, **k: (_ for _ in ()).throw(Exception("no tocar disco")))
    return JUEGOS_FALSOS


@pytest.fixture()
def usuarios_db_con_usuario():
    return {
        "1234": {
            "nombre": "TestUser",
            "contrasena": "pass123",
            "fecha_nacimiento": "01/01/1990",
            "fichas": 500,
            "fecha_registro": "01/01/2024",
            "stats": {
                "partidas_totales": 0,
                "dados": 0,
                "ruleta": 0,
                "tragamonedas": 0,
                "carreras": 0
            }
        }
    }

# ══════════════════════════════════════════════════════════════
# TESTS DE ESTRUCTURA DE JUEGOS
# ══════════════════════════════════════════════════════════════

def test_todos_los_juegos_encontrados(juegos):
    assert len(juegos) > 0, "No hay juegos definidos"


def test_estructura_de_cada_juego(juegos):
    campos_esperados = {"id", "nombre", "descripcion", "apuesta_minima", "reglas"}
    for juego in juegos:
        assert campos_esperados <= juego.keys(), \
            f"Juego {juego.get('id')} le faltan campos: {campos_esperados - juego.keys()}"
        assert "opciones" in juego["reglas"], \
            f"Juego {juego.get('id')} no tiene 'opciones' en reglas"
        assert isinstance(juego["reglas"]["opciones"], list), \
            f"'opciones' debe ser lista en {juego.get('id')}"
        for opcion in juego["reglas"]["opciones"]:
            assert {"tipo", "valores", "pago"} <= opcion.keys(), \
                f"Opción incompleta en {juego.get('id')}: {opcion}"


def test_ids_unicos(juegos):
    ids = [j["id"] for j in juegos]
    assert len(ids) == len(set(ids)), f"Hay IDs duplicados: {ids}"


def test_nombres_unicos(juegos):
    nombres = [j["nombre"] for j in juegos]
    assert len(nombres) == len(set(nombres)), f"Hay nombres duplicados: {nombres}"


def test_apuesta_minima_valida(juegos):
    for juego in juegos:
        ap = juego["apuesta_minima"]
        assert isinstance(ap, (int, float)), f"apuesta_minima no es número en {juego['nombre']}"
        assert ap > 0, f"apuesta_minima debe ser > 0 en {juego['nombre']}"


def test_valores_pago_validos(juegos):
    for juego in juegos:
        for opcion in juego["reglas"]["opciones"]:
            pago = opcion["pago"]
            assert isinstance(pago, (int, float)), f"pago no es número en {juego['nombre']}"
            assert pago >= 1, f"pago debe ser >= 1 en {juego['nombre']}"


def test_descripciones_no_vacias(juegos):
    for juego in juegos:
        assert juego["descripcion"] and len(juego["descripcion"]) > 5, \
            f"Descripción vacía o muy corta en {juego['nombre']}"


def test_opciones_no_vacias(juegos):
    for juego in juegos:
        assert len(juego["reglas"]["opciones"]) > 0, \
            f"El juego {juego['nombre']} no tiene opciones"


def test_valores_de_opciones_no_vacios(juegos):
    for juego in juegos:
        for opcion in juego["reglas"]["opciones"]:
            assert isinstance(opcion["valores"], list) and len(opcion["valores"]) > 0, \
                f"Opción '{opcion['tipo']}' en {juego['nombre']} sin valores"


def test_tipos_de_opciones_validos(juegos):
    for juego in juegos:
        for opcion in juego["reglas"]["opciones"]:
            assert isinstance(opcion["tipo"], str) and len(opcion["tipo"]) > 0, \
                f"Tipo inválido en {juego['nombre']}: {opcion['tipo']}"


# ══════════════════════════════════════════════════════════════
# TESTS DE LA CLASE JUEGO
# ══════════════════════════════════════════════════════════════

def test_creacion_instancia_juego(usuarios_db_con_usuario):
    juego = Juego(
        nombre_juego="dados",
        usuarios=usuarios_db_con_usuario,
        uid="1234",
        gestionar_apuesta=gestionar_apuesta,
        guardar_datos=lambda datos: None
    )
    assert juego.nombre_juego == "dados"
    assert juego.uid == "1234"
    assert "1234" in juego.usuarios


@pytest.mark.parametrize("nombre", ["dados", "ruleta", "tragamonedas", "carreras"])
def test_juego_nombre_correcto(usuarios_db_con_usuario, nombre):
    juego = Juego(
        nombre_juego=nombre,
        usuarios=usuarios_db_con_usuario,
        uid="1234",
        gestionar_apuesta=gestionar_apuesta,
        guardar_datos=lambda datos: None
    )
    assert juego.nombre_juego == nombre


def test_juego_tiene_usuarios(usuarios_db_con_usuario):
    juego = Juego(
        nombre_juego="dados",
        usuarios=usuarios_db_con_usuario,
        uid="1234",
        gestionar_apuesta=gestionar_apuesta,
        guardar_datos=lambda datos: None
    )
    assert len(juego.usuarios) > 0
    assert "1234" in juego.usuarios
    assert juego.usuarios["1234"]["nombre"] == "TestUser"