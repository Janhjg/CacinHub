import os
import time
from Funciones.funciones import crear_usuario, iniciar_sesion, gestionar_apuesta
from Funciones.historial import cargar_json, guardar_json, obtener_historial_usuario
from Funciones.banco import ejecutar_banco
from Funciones.gacha import GachaChistes 
from juegos.carreras import JuegoCarreras 
from juegos.dados import JuegoDados
from juegos.ruleta import JuegoRuleta
from juegos.traga_monedas import JuegoTraga_monedas

DB_PATH = "base_data/users.json"

def guardar_datos_casino(datos_actualizados):
    guardar_json(DB_PATH, datos_actualizados)

def menu_seleccion_juegos(usuarios, uid):
    """Submenú exclusivo para los juegos sin usar break"""
    continuar_juego = True
    while continuar_juego:
        print("\n" + "-"*30)
        print("      ZONA DE JUEGOS")
        print("-" * 30)
        print("1. Dados (Duelo x2)")
        print("2. Carreras de Caballos")
        print("3. Ruleta de la suerte")
        print("4. La Roba Sueldos")
        print("5. Volver al menu anterior")
        
        op_juego = input("Selecciona un juego: ")

        if op_juego == "1":
            juego = JuegoDados(usuarios, uid, gestionar_apuesta, guardar_datos_casino)
            juego.jugar()
        elif op_juego == "2":
            juego = JuegoCarreras(usuarios, uid, gestionar_apuesta, guardar_datos_casino)
            juego.jugar()
        elif op_juego == "3":
            juego = JuegoRuleta(usuarios, uid, gestionar_apuesta, guardar_datos_casino)
            juego.jugar()
        elif op_juego =="4":
            juego = JuegoTraga_monedas(usuarios, uid, gestionar_apuesta, guardar_datos_casino)
            juego.jugar()
        elif op_juego =="5":
            continuar_juego = False 
        else:
            print("Opcion no valida.")

def menu_principal_sesion(usuarios, uid):
    """Menu una vez iniciada la sesion"""
    sesion_activa = True
    
    while sesion_activa:
        nombre = usuarios[uid]['nombre']
        fichas = usuarios[uid]['fichas']
        
        print("\n" + "="*40)
        print("         CASINO CANCINHUB")
        print("="*40)
        print(f"Usuario: {nombre.upper()} | Fichas: {fichas}")
        print("-" * 40)
        print("1. Ir a los juegos")
        print("2. Banco (Obtener fichas)")
        print("3. Gacha de Chistes (Coste: 5)")
        print("4. Ver historial")
        print("5. Cerrar sesion")
        print("-" * 40)
        
        op = input("Selecciona una opcion: ")

        if op == "1":
            menu_seleccion_juegos(usuarios, uid)
        
        elif op == "2":
            ejecutar_banco(usuarios, uid, guardar_datos_casino)

        elif op == "3":
            print(f"\n¿Quieres gastar 5 fichas en un chiste? (Saldo: {fichas})")
            confirmacion = input("Escribe 'S' para confirmar: ").upper()
            
            if confirmacion == "S":
                gacha = GachaChistes(usuarios, uid, guardar_datos_casino)
                resultado = gacha.tirar_gacha()
                
                if "error" in resultado:
                    print(f"\n[ERROR] {resultado['error']}")
                else:
                    print("\nProcesando apuesta...", end="")
                    for _ in range(3):
                        time.sleep(0.5)
                        print(".", end="", flush=True)
                    
                    print(f"\n\n--- CHISTE ---")
                    print(f"'{resultado['chiste']}'")
                    print(f"--------------")
                    print(f"Fichas restantes: {resultado['fichas_restantes']}")
            else:
                print("\nDecidiste guardar tus fichas.")
            
        elif op == "4":
            perfil = obtener_historial_usuario(uid)
            if perfil:
                print(f"\n--- ESTADISTICAS DE {perfil['usuario']} ---")
                print(f"Fichas: {perfil['fichas_actuales']}")
                for p in perfil['ultimas_partidas']:
                    print(f"{p['fecha']} | {p['juego']}: {p['resultado']} ({p['ganancia']})")
            else:
                print("\nSin historial.")

        elif op == "5":
            print(f"\n¡Hasta pronto, {nombre}!")
            sesion_activa = False 
        else:
            print("Opcion no valida.")

def main():
    ejecutando_programa = True
    
    while ejecutando_programa:
        usuarios = cargar_json(DB_PATH)
        
        print("\n" + "="*30)
        print("CANCIN-HUB - Casino Virtual")
        print("="*30)
        print("1. Crear Cuenta")
        print("2. Entrar (Login)")
        print("3. Salir del Casino")
        op = input("> ")
        
        if op == "1":
            nombre = input("Nombre de usuario: ")
            password = input("Contrasena: ")
            usuarios = crear_usuario(usuarios, nombre, password)
            guardar_json(DB_PATH, usuarios)
            
        elif op == "2":
            uid = input("ID: ")
            password = input("Contrasena: ")
            
            if iniciar_sesion(usuarios, uid, password):
                menu_principal_sesion(usuarios, uid)
                
        elif op == "3":
            print("\nSaliendo del sistema...")
            ejecutando_programa = False 
        else:
            print("Opcion no valida.")

if __name__ == "__main__":
    main()