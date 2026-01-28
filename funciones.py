import random
import time

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