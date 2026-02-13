import random
from juegos.base_juegos import *

class JuegoCarreras(Juego):
    def __init__(self, usuarios, uid, gestionar_apuesta, guardar_datos):
        super().__init__("carreras", usuarios, uid, gestionar_apuesta, guardar_datos)
        
        self.caballos = {
            "1": {"nombre": "Secretariat", "prob": 40, "mult": 2},
            "2": {"nombre": "Tamamo Cross", "prob": 30, "mult": 3},
            "3": {"nombre": "Epona", "prob": 20, "mult": 4},
            "4": {"nombre": "Tormenta China", "prob": 10, "mult": 5}
        }

    def mostrar_menu_caballos(self):
        print("\n" + "="*35)
        print("--- BIENVENIDO AL HIPODROMO ---")
        print("="*35)
        for k, v in self.caballos.items():
            print(f"{k}. {v['nombre']} | x{v['mult']} (Exito: {v['prob']}%)")
        print("-" * 35)

    def jugar(self):
        self.mostrar_menu_caballos()
        
        eleccion = input("\nSelecciona tu caballo (1-4): ")
        if eleccion not in self.caballos:
            print("Seleccion no valida. Volviendo al menu.")
            return

        apuesta = self.solicitar_apuesta()
        
        if apuesta:
            caballo_elegido = self.caballos[eleccion]["nombre"]
            
            self.animacion_espera(f"Se abren los partidores! Galopando con {caballo_elegido}...")

            azar = random.randint(1, 100)
            if azar <= 40: 
                ganador_id = "1"
            elif azar <= 70: 
                ganador_id = "2"
            elif azar <= 90: 
                ganador_id = "3"
            else: 
                ganador_id = "4"

            ganador_nombre = self.caballos[ganador_id]["nombre"]
            print(f"RESULTADO: El ganador es {ganador_nombre.upper()}!")

            gano = (eleccion == ganador_id)
            multiplicador = self.caballos[eleccion]["mult"]
            
            detalle_partida = f"Aposto por {caballo_elegido}. Ganador: {ganador_nombre}"

            self.procesar_resultado(apuesta, gano, multiplicador, detalle_partida)

            if gano:
                print(f"Felicidades! Has ganado {apuesta * multiplicador} fichas.")
            else:
                print("Tu caballo no logro el primer puesto. Suerte para la proxima.")