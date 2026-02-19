import random
from juegos.base_juegos import *

class JuegoDados(Juego):
    def __init__(self, usuarios, uid, gestionar_apuesta, guardar_datos):
        super().__init__("dados", usuarios, uid, gestionar_apuesta, guardar_datos)

    def jugar(self):
        print("\n" + "="*35)
        print("--- DUELO DE DADOS CONTRA LA BANCA ---")
        print("="*35)

        apuesta = self.solicitar_apuesta()
        
        if apuesta:
            self.animacion_espera("Lanzando los dados sobre el tapete...")

            tiro_jugador = random.randint(1, 6)
            tiro_banca = random.randint(1, 6)

            print(f"-> Tu dado:  [{tiro_jugador}]")
            print(f"-> Banca:    [{tiro_banca}]")
            print("-" * 35)

            detalle_duelo = f"Jugador: {tiro_jugador} vs Banca: {tiro_banca}"

            if tiro_jugador > tiro_banca:
                print("HAS GANADO! La banca paga el doble.")
                self.procesar_resultado(apuesta, True, 2, detalle_duelo)
                
            elif tiro_banca > tiro_jugador:
                print("LA BANCA GANA. Has perdido tu apuesta.")
                self.procesar_resultado(apuesta, False, 0, detalle_duelo)
                
            else:
                print("EMPATE! Se te devuelven tus fichas.")
                self.procesar_resultado(apuesta, True, 1, "Empate tecnico")

            print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")