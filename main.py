import json
import os
from funciones import crear_usuario, iniciar_sesion, gestionar_apuesta
from juegos.dados import jugar_dados
from juegos.carreras import jugar_carreras

DB_PATH = "base_data/users.json"

def cargar_datos():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f: return json.load(f)
    return {}

def guardar_datos(datos):
    with open(DB_PATH, "w", encoding="utf-8") as f: json.dump(datos, f, indent=4)

def menu_juegos(usuarios, uid):
    while True:
        print(f"\n--- CASINO CANCINHUB (ID: {uid} | Fichas: {usuarios[uid]['fichas']}) ---")
        print("1. Dados (x2)")
        print("2. Carreras (Variable)")
        print("3. Cerrar Sesión")
        op = input("Selecciona: ")
        
        if op == "1":
            jugar_dados(usuarios, uid, gestionar_apuesta, guardar_datos)
        elif op == "2":
            jugar_carreras(usuarios, uid, gestionar_apuesta, guardar_datos)
        elif op == "3":
            break

def main():
    usuarios = cargar_datos()
    while True:
        print("\n=== CACINHUB ===")
        print("1. Crear Cuenta")
        print("2. Entrar")
        print("3. Salir")
        op = input("> ")
        
        if op == "1":
            n, p = input("Nombre: "), input("Contraseña: ")
            usuarios = crear_usuario(usuarios, n, p)
            guardar_datos(usuarios)
        elif op == "2":
            uid, p = input("ID: "), input("Pass: ")
            if iniciar_sesion(usuarios, uid, p):
                menu_juegos(usuarios, uid)
        elif op == "3": break

if __name__ == "__main__":
    main()