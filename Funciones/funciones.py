import random
import json
from datetime import datetime

class Usuario:
    def __init__(self, nombre, contrasena, fecha_nacimiento, id_usuario=None, fichas=100, fecha_reg=None, stats=None):
        self.nombre = nombre
        self.contrasena = contrasena
        self.fecha_nacimiento = fecha_nacimiento
        self.id = id_usuario if id_usuario else str(random.randint(1000, 9999))
        self._fichas = fichas
        self.fecha_registro = fecha_reg if fecha_reg else datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.stats = stats if stats else {
            "partidas_totales": 0, "dados": 0, "ruleta": 0, "tragamonedas": 0, "carreras": 0
        }

    @property
    def fichas(self):
        return self._fichas

    @fichas.setter
    def fichas(self, cantidad):
        if cantidad < 0:
            self._fichas = 0
        else:
            self._fichas = cantidad

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "contrasena": self.contrasena,
            "fecha_nacimiento": self.fecha_nacimiento,
            "fichas": self.fichas,
            "fecha_registro": self.fecha_registro,
            "stats": self.stats
        }

def calcular_edad(fecha_str):
    try:
        nacimiento = datetime.strptime(fecha_str, "%d/%m/%Y")
        hoy = datetime.now()
        edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        return edad
    except ValueError:
        return None

def crear_usuario(usuarios_db, nombre, contrasena):
    print("\n--- REGISTRO DE EDAD ---")
    fecha_nac = input("Introduce tu fecha de nacimiento (DD/MM/YYYY): ")
    
    edad = calcular_edad(fecha_nac)
    
    if edad is None:
        print("Error: Formato de fecha no válido.")
        return usuarios_db
        
    if edad < 18:
        print(f"Acceso denegado: Tienes {edad} años. Solo mayores de 18.")
        return usuarios_db

    while True:
        nuevo_user = Usuario(nombre, contrasena, fecha_nac)
        if nuevo_user.id not in usuarios_db:
            break
    
    usuarios_db[nuevo_user.id] = nuevo_user.to_dict()
    print(f"\nUsuario creado: {nuevo_user.nombre}")
    print(f"ID: {nuevo_user.id} | Edad: {edad} años")
    print(f"Registro: {nuevo_user.fecha_registro}")
    return usuarios_db

def iniciar_sesion(usuarios_db, usuario_id, contrasena):
    if usuario_id in usuarios_db:
        if usuarios_db[usuario_id]["contrasena"] == contrasena:
            print(f"\n¡Hola de nuevo, {usuarios_db[usuario_id]['nombre']}!")
            return True
        print("\nContraseña incorrecta.")
    else:
        print("\nID no encontrado.")
    return False

def gestionar_apuesta(usuarios, uid, monto_apuesta, juego, gano, multiplicador):
    """Esta funcion obtiene un usuario, su uid, la cantidad apostada, resultado 
    del juego y multiplicador. A partir de estos datos:
    1.-Descuenta la cantidad apostada de lo que tenga el usuario
    2.- En funcion de si ha ganado y el multiplicador anade la cantidad apostada por 
    el multiplicador
    3.- Si el usuario ha perdido no gana nada"""
    
    uid = str(uid)
    
    usuarios[uid]["fichas"] -= monto_apuesta

    if gano:
        if multiplicador > 1:
            premio = monto_apuesta * multiplicador
            usuarios[uid]["fichas"] += premio
        elif multiplicador == 1: 
            usuarios[uid]["fichas"] += monto_apuesta

    if "stats" not in usuarios[uid]:
        usuarios[uid]["stats"] = {"partidas_totales": 0, "dados": 0, "ruleta": 0, "tragamonedas": 0, "carreras": 0}
    
    usuarios[uid]["stats"]["partidas_totales"] += 1
    if juego in usuarios[uid]["stats"]:
        usuarios[uid]["stats"][juego] += 1
          
    return usuarios