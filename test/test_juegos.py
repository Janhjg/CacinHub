import json

# Ruta del archivo JSON
games_path = "./base_data/games.json"

# Función para cargar juegos
def cargar_juegos():
    with open(games_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("juegos", [])  # devuelve la lista bajo "juegos"

# ----------------------------
# Tests de juegos
# ----------------------------

def test_todos_los_juegos_encontrados():
    juegos = cargar_juegos()
    assert len(juegos) > 0, "No se encontraron juegos en la base de datos"

def test_estructura_de_cada_juego():
    juegos = cargar_juegos()
    campos_esperados = {"id", "nombre", "descripcion", "apuesta_minima", "reglas"}

    for juego in juegos:

        # Verifica que existan todos los campos principales
        assert campos_esperados <= juego.keys(), f"El juego {juego.get('id')} no tiene todos los campos esperados"

        # Verifica que 'reglas' tenga 'opciones' como lista
        assert "opciones" in juego["reglas"], f"El juego {juego.get('id')} no tiene 'opciones' en reglas"
        assert isinstance(juego["reglas"]["opciones"], list), f"'opciones' debe ser una lista en {juego.get('id')}"

        # Verifica cada opción dentro de 'opciones'
        for opcion in juego["reglas"]["opciones"]:
            campos_opcion = {"tipo", "valores", "pago"}
            assert campos_opcion <= opcion.keys(), f"Opción incompleta en {juego.get('id')}"

# Verifica que no haya juegos con nombres no verificados con antelacion 
def test_sin_juegos_no_verificados():
    juegos = cargar_juegos()

    nombres_permitidos = {
        "Dados",
        "Ruleta",
        "Tragamonedas",
        "Carrera de Caballos",
    }

    assert all(
        juego["nombre"] in nombres_permitidos
        for juego in juegos
    ), "Se encontró un juego con un nombre no permitido"
