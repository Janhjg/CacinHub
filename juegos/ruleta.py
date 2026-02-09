import random
from juegos.base_juegos import *

class JuegoRuleta(Juego):
    def __init__(self, usuarios, uid, gestionar_apuesta, guardar_datos):
        super().__init__("ruleta", usuarios, uid, gestionar_apuesta, guardar_datos)

        # Números válidos de la ruleta
        self.numeros = list(range(0, 37))

        # Pares e impares
        self.pares = [n for n in self.numeros if n % 2 == 0]
        self.impares = [n for n in self.numeros if n % 2 != 0]

    def jugar(self):
        print("\n" + "="*35)
        print("--- RULETA DE LA SUERTE ---")
        print("="*35)

        print("\nTipo de apuesta:")
        print("1 - Número (0 al 36)")
        print("2 - Pares")
        print("3 - Impares")

        eleccion = input("\nElija una opción (1/2/3): ")

        if eleccion not in ("1", "2", "3"):
            print("Selección no válida. Volviendo al menú.")
            return

        if eleccion == "1":
            try:
                numero = int(input("Elija un número del 0 al 36: "))
            except ValueError:
                print("Entrada inválida.")
                return

            if numero not in self.numeros:
                print("Número fuera de rango.")
                return

            tipo_apuesta = numero

        elif eleccion == "2":
            tipo_apuesta = "pares"

        else:  # eleccion == "3"
            tipo_apuesta = "impares"

        apuesta = self.solicitar_apuesta()

        print(f"Apuesta realizada a: {tipo_apuesta} por {apuesta}")
