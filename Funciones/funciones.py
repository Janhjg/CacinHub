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

def gestionar_apuesta(usuarios_db, usuario_id, monto, juego, gano, multiplicador=2):
    datos = usuarios_db[usuario_id]
    
    user = Usuario(
        datos["nombre"], datos["contrasena"], datos["fecha_nacimiento"],
        usuario_id, datos["fichas"], datos["fecha_registro"], datos["stats"]
    )
    
    if gano:
        user.fichas += (monto * multiplicador)
    
    user.stats["partidas_totales"] += 1
    if juego in user.stats:
        user.stats[juego] += 1

    usuarios_db[usuario_id] = user.to_dict()
    return usuarios_db