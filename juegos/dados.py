import random
import time

def jugar_dados(usuarios, uid, gestionar_apuesta, guardar_datos):
    print("\n" + "="*25)
    print("--- DUELO DE DADOS CONTRA LA BANCA ---")
    print("="*25)
    
    fichas_actuales = usuarios[uid]["fichas"]
    
    try:
        apuesta = int(input(f"Saldo: {fichas_actuales} | ¿Cuánto apuestas?: "))
        
        if apuesta <= 0 or apuesta > fichas_actuales:
            print("Cantidad no válida o saldo insuficiente.")
            return

        """Retiro preventivo de fichas"""
        usuarios[uid]["fichas"] -= apuesta
        
        print("\nLanzando dados...")
        time.sleep(0.5)
        
        tiro_jugador = random.randint(1, 6)
        tiro_banca = random.randint(1, 6)
        
        print(f"➤ Tu dado:  [{tiro_jugador}]")
        print(f"➤ Banca:    [{tiro_banca}]")
        print("-" * 25)

        if tiro_jugador > tiro_banca:
            print(f"¡GANASTE!")
            usuarios = gestionar_apuesta(usuarios, uid, apuesta, "dados", True, 2)
            
        elif tiro_banca > tiro_jugador:
            print("LA BANCA GANA.")
            usuarios = gestionar_apuesta(usuarios, uid, apuesta, "dados", False)
            
        else:
            print("¡EMPATE! Se te devuelven las fichas.")
            """Aquí estaba el fallo, ahora corregido:"""
            usuarios[uid]["fichas"] += apuesta
            usuarios[uid]["stats"]["partidas_totales"] += 1
            usuarios[uid]["stats"]["dados"] += 1

        guardar_datos(usuarios)
        print(f"Saldo final: {usuarios[uid]['fichas']} fichas.")

    except ValueError:
        print("Error: Introduce un número entero para la apuesta.")