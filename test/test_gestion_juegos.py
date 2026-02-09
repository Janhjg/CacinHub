import json
import pytest
from Funciones.funciones import *
from juegos.base_juegos import Juego
import os

@pytest.fixture
def usuarios_db_con_usuario():
    """Crea un usuario de prueba"""
    usuario_test = Usuario("TestUser", "pass123", "01/01/2000", id_usuario="1234", fichas=100)
    return {"1234": usuario_test.to_dict()}


def cargar_juegos():
    """Carga los juegos desde el archivo JSON"""
    ruta_archivo = "base_data/games.json"
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("juegos", [])


# =====================================================
# TESTS DE ESTRUCTURA DE DATOS DE JUEGOS
# =====================================================

def test_archivo_games_existe():
    """Verifica que el archivo games.json existe y es accesible"""
    try:
        juegos = cargar_juegos()
        assert True, "Archivo encontrado y cargado correctamente"
    except FileNotFoundError as e:
        pytest.fail(f"Archivo games.json no encontrado: {e}")


def test_todos_los_juegos_encontrados():
    """Verifica que hay juegos disponibles en games.json"""
    juegos = cargar_juegos()
    assert len(juegos) > 0, "No se encontraron juegos en la base de datos"

def test_estructura_de_cada_juego():
    """Verifica que cada juego tiene la estructura correcta"""
    juegos = cargar_juegos()
    campos_esperados = {"id", "nombre", "descripcion", "apuesta_minima", "reglas"}

    for juego in juegos:
        # Verifica que existan todos los campos principales
        assert campos_esperados <= juego.keys(), \
            f"El juego {juego.get('id')} no tiene todos los campos esperados. " \
            f"Tiene: {juego.keys()}, Esperados: {campos_esperados}"

        # Verifica que 'reglas' tenga 'opciones' como lista
        assert "opciones" in juego["reglas"], \
            f"El juego {juego.get('id')} no tiene 'opciones' en reglas"
        
        assert isinstance(juego["reglas"]["opciones"], list), \
            f"'opciones' debe ser una lista en {juego.get('id')}"

        # Verifica cada opción dentro de 'opciones'
        for opcion in juego["reglas"]["opciones"]:
            campos_opcion = {"tipo", "valores", "pago"}
            assert campos_opcion <= opcion.keys(), \
                f"Opción incompleta en {juego.get('id')}. " \
                f"Tiene: {opcion.keys()}, Esperados: {campos_opcion}"


def test_sin_juegos_no_verificados():
    """Verifica que no haya juegos con nombres no permitidos"""
    juegos = cargar_juegos()

    nombres_permitidos = {
        "dados",
        "ruleta",
        "tragamonedas",
        "carreras_de_caballos",
    }

    for juego in juegos:
        assert juego["nombre"] in nombres_permitidos, \
            f"Se encontró un juego con nombre no permitido: '{juego['nombre']}'. " \
            f"Nombres permitidos: {nombres_permitidos}"


def test_ids_unicos():
    """Verifica que cada juego tiene un ID único"""
    juegos = cargar_juegos()
    
    ids = [juego["id"] for juego in juegos]
    
    assert len(ids) == len(set(ids)), \
        f"Hay IDs duplicados en los juegos. IDs encontrados: {ids}"


def test_nombres_unicos():
    """Verifica que cada juego tiene un nombre único"""
    juegos = cargar_juegos()
    
    nombres = [juego["nombre"] for juego in juegos]
    
    assert len(nombres) == len(set(nombres)), \
        f"Hay nombres duplicados en los juegos. Nombres encontrados: {nombres}"


def test_apuesta_minima_valida():
    """Verifica que todos los juegos tienen apuesta mínima válida"""
    juegos = cargar_juegos()
    
    for juego in juegos:
        apuesta_min = juego["apuesta_minima"]
        
        assert isinstance(apuesta_min, (int, float)), \
            f"apuesta_minima debe ser número en {juego['nombre']}"
        
        assert apuesta_min > 0, \
            f"apuesta_minima debe ser mayor que 0 en {juego['nombre']}"


def test_valores_pago_validos():
    """Verifica que todos los pagos son valores válidos"""
    juegos = cargar_juegos()
    
    for juego in juegos:
        for opcion in juego["reglas"]["opciones"]:
            pago = opcion["pago"]
            
            assert isinstance(pago, (int, float)), \
                f"El pago debe ser número en {juego['nombre']}"
            
            assert pago >= 1, \
                f"El pago debe ser >= 1 en {juego['nombre']}"


def test_descripciones_no_vacias():
    """Verifica que todos los juegos tienen descripción"""
    juegos = cargar_juegos()
    
    for juego in juegos:
        assert juego["descripcion"], \
            f"El juego {juego['nombre']} no tiene descripción"
        
        assert len(juego["descripcion"]) > 5, \
            f"La descripción de {juego['nombre']} es demasiado corta"


def test_opciones_no_vacias():
    """Verifica que todos los juegos tienen al menos una opción"""
    juegos = cargar_juegos()
    
    for juego in juegos:
        opciones = juego["reglas"]["opciones"]
        
        assert len(opciones) > 0, \
            f"El juego {juego['nombre']} no tiene opciones"


def test_valores_de_opciones_no_vacios():
    """Verifica que todas las opciones tienen valores"""
    juegos = cargar_juegos()
    
    for juego in juegos:
        for opcion in juego["reglas"]["opciones"]:
            valores = opcion["valores"]
            
            assert isinstance(valores, list), \
                f"Los valores deben ser una lista en {juego['nombre']}"
            
            assert len(valores) > 0, \
                f"La opción '{opcion['tipo']}' en {juego['nombre']} no tiene valores"


def test_tipos_de_opciones_validos():
    """Verifica que los tipos de opciones son strings válidos"""
    juegos = cargar_juegos()
    
    for juego in juegos:
        for opcion in juego["reglas"]["opciones"]:
            tipo = opcion["tipo"]
            
            assert isinstance(tipo, str), \
                f"El tipo debe ser string en {juego['nombre']}"
            
            assert len(tipo) > 0, \
                f"El tipo no puede estar vacío en {juego['nombre']}"


# =====================================================
# TESTS DE LA CLASE JUEGO
# =====================================================

def test_creacion_instancia_juego(usuarios_db_con_usuario):
    """Verifica que se puede crear una instancia de la clase Juego"""
    
    def mock_guardar(datos):
        pass
    
    juego = Juego(
        nombre_juego="dados",
        usuarios=usuarios_db_con_usuario,
        uid="1234",
        gestionar_apuesta=gestionar_apuesta,
        guardar_datos=mock_guardar
    )
    
    assert juego.nombre_juego == "dados"
    assert juego.uid == "1234"
    assert "1234" in juego.usuarios


def test_juego_nombre_correcto(usuarios_db_con_usuario):
    """Verifica que el juego guarda el nombre correctamente"""
    
    def mock_guardar(datos):
        pass
    
    juegos_nombres = ["dados", "ruleta", "tragamonedas", "carreras"]
    
    for nombre in juegos_nombres:
        juego = Juego(
            nombre_juego=nombre,
            usuarios=usuarios_db_con_usuario,
            uid="1234",
            gestionar_apuesta=gestionar_apuesta,
            guardar_datos=mock_guardar
        )
        
        assert juego.nombre_juego == nombre


def test_juego_tiene_usuarios(usuarios_db_con_usuario):
    """Verifica que el juego tiene acceso a los usuarios"""
    
    def mock_guardar(datos):
        pass
    
    juego = Juego(
        nombre_juego="dados",
        usuarios=usuarios_db_con_usuario,
        uid="1234",
        gestionar_apuesta=gestionar_apuesta,
        guardar_datos=mock_guardar
    )
    
    assert len(juego.usuarios) > 0
    assert "1234" in juego.usuarios
    assert juego.usuarios["1234"]["nombre"] == "TestUser"

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