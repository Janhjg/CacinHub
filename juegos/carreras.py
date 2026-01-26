import random
import time

def jugar_carreras(usuarios, uid, gestionar_apuesta, guardar_datos):
    print("\n" + "="*30)
    print("--- BIENVENIDO AL HIPÓDROMO ---")
    print("="*30)
    
    caballos = {
        "1": {"nombre": "Secretariat", "prob": 40, "mult": 2},
        "2": {"nombre": "Tamamo Cross", "prob": 30, "mult": 3},
        "3": {"nombre": "Epona", "prob": 20, "mult": 4},
        "4": {"nombre": "Tormenta China", "prob": 10, "mult": 5}
    }

    for k, v in caballos.items():
        print(f"{k}. {v['nombre']} | Premio: x{v['mult']} (Éxito: {v['prob']}%)")

    eleccion = input("\nSelecciona tu caballo (1-4): ")
    if eleccion not in caballos:
        print("Selección no válida.")
        return

    try:
        apuesta = int(input(f"¿Cuánto apuestas a {caballos[eleccion]['nombre']}?: "))
        if apuesta <= 0 or apuesta > usuarios[uid]["fichas"]:
            print("Saldo insuficiente o cantidad inválida.")
            return

        """Retiro preventivo de fichas"""
        usuarios[uid]["fichas"] -= apuesta
        print(f"\n¡Se abren los partidores! Has apostado {apuesta} fichas.")
        
        """Animación simple"""
        for i in range(3):
            print("... Galopando ...")
            time.sleep(0.5)

        """Lógica de probabilidad acumulada"""
        resultado_azar = random.randint(1, 100)
        if resultado_azar <= 40: ganador = "1"
        elif resultado_azar <= 70: ganador = "2"
        elif resultado_azar <= 90: ganador = "3"
        else: ganador = "4"

        print(f"\n¡EL GANADOR ES {caballos[ganador]['nombre'].upper()}!")

        gano = (eleccion == ganador)
        
        """Procesa el resultado con la función"""
        usuarios = gestionar_apuesta(
            usuarios, uid, apuesta, "carreras", gano, caballos[eleccion]["mult"]
        )
        
        if gano:
            premio = apuesta * caballos[eleccion]["mult"]
            print(f"¡Felicidades! Ganaste {premio} fichas.")
        else:
            print("Tu caballo no llegó primero. ¡Más suerte la próxima!")

        guardar_datos(usuarios)
        print(f"Saldo actual: {usuarios[uid]['fichas']} fichas.")

    except ValueError:
        print("Error: Introduce un número entero para la apuesta.")