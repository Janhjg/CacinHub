import os
from Funciones.funciones import crear_usuario, iniciar_sesion, gestionar_apuesta
from Funciones.historial import cargar_json, guardar_json, obtener_historial_usuario
from Funciones.banco import ejecutar_banco
from juegos.carreras import JuegoCarreras 
from juegos.dados import JuegoDados

DB_PATH = "base_data/users.json"

def guardar_datos_casino(datos_actualizados):
    guardar_json(DB_PATH, datos_actualizados)

def menu_juegos(usuarios, uid):
    sesion_activa = True
    
    while sesion_activa:
        nombre = usuarios[uid]['nombre']
        fichas = usuarios[uid]['fichas']
        
        print("\n" + "="*40)
        print("         CASINO CANCINHUB")
        print("="*40)
        print(f"Usuario: {nombre.upper()} | Saldo: {fichas} fichas")
        print("-" * 40)
        print("1. Dados (Duelo contra la banca x2)")
        print("2. Carreras de Caballos (Hipodromo)")
        print("3. Banco (Obtener fichas)")
        print("4. Gacha de Chistes (Probar suerte)")
        print("5. Ver mi Historial y Perfil")
        print("6. Cerrar Sesion")
        print("-" * 40)
        
        op = input("Selecciona una opcion: ")

        if op == "1":
            juego = JuegoDados(usuarios, uid, gestionar_apuesta, guardar_datos_casino)
            juego.jugar()
        
        elif op == "2":
            juego = JuegoCarreras(usuarios, uid, gestionar_apuesta, guardar_datos_casino)
            juego.jugar()

        elif op == "3":
            ejecutar_banco(usuarios, uid, guardar_datos_casino)
            
        elif op == "4":
            print("\n[INFO] La Gacha de Chistes esta en mantenimiento.")
            
        elif op == "5":
            perfil = obtener_historial_usuario(uid)
            if perfil:
                print(f"\n--- ESTADISTICAS DE {perfil['usuario']} ---")
                print(f"Saldo actual: {perfil['fichas_actuales']} fichas")
                print(f"Partidas jugadas: {perfil['stats']['partidas_totales']}")
                print("\nUltimos 5 movimientos:")
                for p in perfil['ultimas_partidas']:
                    if p['resultado'] == "gano":
                        simb = "[+]"
                    elif p['resultado'] == "perdio":
                        simb = "[-]"
                    else:
                        simb = "[=]"
                    
                    print(f"{simb} {p['fecha']} | {p['juego'].capitalize()}: {p['resultado']} ({p['ganancia']} fichas)")
            else:
                print("\nAun no tienes partidas registradas.")

        elif op == "6":
            print(f"\nSaliendo... Hasta pronto {nombre}!")
            sesion_activa = False
        else:
            print("Opcion no valida. Intenta de nuevo.")

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
            uid = input("Introduce tu ID: ")
            password = input("Introduce tu contrasena: ")
            
            if iniciar_sesion(usuarios, uid, password):
                menu_juegos(usuarios, uid)
                
        elif op == "3":
            print("\nApagando maquinas... Gracias por jugar!")
            ejecutando_programa = False
        else:
            print("Opcion no valida.")

if __name__ == "__main__":
    main()