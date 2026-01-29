import random
import time
import json
from datetime import datetime

def crear_usuario(usuarios_db, nombre, contrasena):
    while True:
        nuevo_id = str(random.randint(1000, 9999))
        if nuevo_id not in usuarios_db:
            break
    
    usuario = {
        "nombre": nombre,
        "contrasena": contrasena,
        "fichas": 100,
        "fecha_registro": time.ctime(),
        "stats": {
            "partidas_totales": 0,
            "dados": 0,
            "ruleta": 0,
            "tragamonedas": 0,
            "carreras": 0
        }
    }
    
    usuarios_db[nuevo_id] = usuario

    print(f"\nUsuario creado con éxito. Tu ID de acceso es: {nuevo_id}")
    return usuarios_db

def iniciar_sesion(usuarios_db, usuario_id, contrasena):
    if usuario_id in usuarios_db:
        if usuarios_db[usuario_id]["contrasena"] == contrasena:
            print(f"\n¡Bienvenido de nuevo, {usuarios_db[usuario_id]['nombre']}!")
            return True
        else:
            print("\nContraseña incorrecta.")
    else:
        print("\nEl ID de usuario no existe.")
    return False

def gestionar_apuesta(usuarios_db, usuario_id, monto, juego, gano, multiplicador=2):
    user = usuarios_db[usuario_id]
    
    if gano:
        user["fichas"] += (monto * multiplicador)
    
    user["stats"]["partidas_totales"] += 1
    if juego in user["stats"]:
        user["stats"][juego] += 1

    return usuarios_db

# ----------------
# Historial
# ---------------

def cargar_usuarios():
    # Carga users.json
    with open("base_data/users.json", "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_usuarios(datos):
    # Guarda users.json
    with open("base_data/users.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def obtener_usuario(user_id):
    # Obtiene un usuario por su ID
    usuarios_db = cargar_usuarios()
    user_key = str(user_id)
    
    if user_key in usuarios_db:
        # Devolver usuario con su ID incluido
        usuario = usuarios_db[user_key].copy()
        usuario["id"] = user_id
        return usuario
    return None

def actualizar_fichas(user_id, nuevas_fichas):
    # Actualiza las fichas del usuario
    usuarios_db = cargar_usuarios()
    user_key = str(user_id)
    
    if user_key in usuarios_db:
        usuarios_db[user_key]["fichas"] = nuevas_fichas
        guardar_usuarios(usuarios_db)
        return True
    return False

def actualizar_stats(user_id, juego):
    # Actualiza los stats del usuario (partidas totales y por juego)
    usuarios_db = cargar_usuarios()
    user_key = str(user_id)
    
    if user_key in usuarios_db:
        # Incrementar partidas totales
        usuarios_db[user_key]["stats"]["partidas_totales"] += 1
        
        # Incrementar contador del juego
        if juego in usuarios_db[user_key]["stats"]:
            usuarios_db[user_key]["stats"][juego] += 1
        
        guardar_usuarios(usuarios_db)
        return True
    return False

# --- 
# Ahora Historial.json
# ---

def cargar_historial():
    with open("base_data/historial.json", "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_historial(datos):
    """Guarda historial.json"""
    with open("base_data/historial.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def registrar_partida(user_id,usuario,juego,apuesta,detalles,resultado,ganancia,fichas_anteriores,fichas_nuevas):
    
    historial = cargar_historial()
    
    # Ver si existe ya
    if "historial_usuarios" not in historial:
        historial["historial_usuarios"] = {}
    
    user_key = str(user_id)
    
    # Iniciar historial del usuario
    if user_key not in historial["historial_usuarios"]:
        historial["historial_usuarios"][user_key] = []
    
    # Crear registro de partida
    partida = {
        "usuario": usuario,
        "juego": juego,
        "apuesta": apuesta,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "detalles": detalles,
        "resultado": resultado,
        "ganancia": ganancia,
        "fichas_anteriores": fichas_anteriores,
        "fichas_nuevas": fichas_nuevas
    }
    
    # Añadir partida
    historial["historial_usuarios"][user_key].append(partida)
    
    # MANTENER SOLO LAS ÚLTIMAS 5 PARTIDAS
    if len(historial["historial_usuarios"][user_key]) > 5:
        historial["historial_usuarios"][user_key] = historial["historial_usuarios"][user_key][-5:]
    
    # Guardar
    guardar_historial(historial)
    
    # ACTUALIZAR STATS EN users.json
    actualizar_stats(user_id, juego)
    
    print(f" Partida registrada para {usuario}")
    
    return partida

def obtener_historial_usuario(user_id):
    
    # datos del usuario
    usuario = obtener_usuario(user_id)
    if not usuario:
        return None
    
    # historial
    historial = cargar_historial()
    user_key = str(user_id)
    partidas = historial.get("historial_usuarios", {}).get(user_key, [])
    
    return {
        "usuario": usuario["nombre"],
        "fichas_actuales": usuario["fichas"],
        "stats": usuario["stats"],
        "ultimas_partidas": partidas
    }
