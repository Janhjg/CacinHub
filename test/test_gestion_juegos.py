import json

# Ruta del archivo JSON
games_path = "games.json"

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
        "dados",
        "ruleta",
        "tragamonedas",
        "carreras_de_caballos",
    }

    assert all(
        juego["nombre"] in nombres_permitidos
        for juego in juegos
    ), "Se encontró un juego con un nombre no permitido"
    

# --------------
# TEST HISTORIAL
# --------------
def test_historial():
    def usuario_con_partidas():
        # Crea un usuario con partidas de prueba 
        
        usuario = crear_usuario("TestHistorial", "pass123", 100)
        user_id = usuario["id"]
        
    def test_historial_completo():
        # 1. Crear un usuario y hacer varias partidas
        usuario = crear_usuario("JugadorTest", "pass123", 500)
        user_id = usuario["id"]
        
        realizar_apuesta(user_id, "dados", 10)
        realizar_apuesta(user_id, "ruleta", 20)
        realizar_apuesta(user_id, "tragamonedas", 15)
        
        # 2. Obtener el historial
        historial = obtener_historial(user_id)
        
        # 3. Verificar que están todas las partidas
        assert len(historial) == 3
        
        # 4. Verificar que cada partida tiene todos los campos
        for partida in historial:
            assert "fecha" in partida
            assert "juego" in partida
            assert "apuesta" in partida
            assert "resultado" in partida
            assert "ganancia" in partida
            assert "saldo" in partida



    def test_limite_resultados():
        
        # 1. Crear usuario con 5 partidas
        usuario = crear_usuario("JugadorTest2", "pass123", 500)
        user_id = usuario["id"]
        
        for i in range(5):
            realizar_apuesta(user_id, "dados", 10)
        
        # 2. Obtener historial con límite de 3
        historial = obtener_historial(user_id, limite=3)
        
        # 3. Verificar que respeta el límite
        assert len(historial) <= 3


    def test_error_usuario_inexistente():
        # 1. Intentar obtener historial de un ID que no existe
         user_id_falso = "id_inexistente_999"
        
        # 2. Verificar que lanza error
         with pytest.raises(Exception):
             obtener_historial(user_id_falso)
        

    def test_usuario_sin_partidas():
        # 1. Crear usuario nuevo sin partidas
         usuario = crear_usuario("UsuarioNuevo", "pass123", 100)
         user_id = usuario["id"]
        
        # 2. Obtener historial
         historial = obtener_historial(user_id)
        
        # 3. Verificar que es un array vacío
         assert historial == []
         assert len(historial) == 0