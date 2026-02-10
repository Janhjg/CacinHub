import random
from juegos.base_juegos import *

class JuegoRuleta(Juego):
    def __init__(self, usuarios, uid, gestionar_apuesta, guardar_datos):
        super().__init__("ruleta", usuarios, uid, gestionar_apuesta, guardar_datos)

        # Números válidos de la ruleta
        self.numeros = list(range(0, 37))

        # Pares e impares
        self.rojo = [n % 2 == 0 for n in self.numeros]
        self.negro = [n % 2 != 0 for n in self.numeros]

    def jugar(self):
        print("\n" + "="*35)
        print("--- RULETA DE LA SUERTE ---")
        print("="*35)

        apuesta = self.solicitar_apuesta()

        print("\nTipo de apuesta:")
        print("1 - Número (0 al 36)")
        print("2 - Pares")
        print("3 - Impares")

        eleccion = input("\nElija una opción (1/2/3): ")
        numero = None

        if eleccion not in ("1", "2", "3"):
            print("Selección no válida.")
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

        ruleta = random.randint(0, 36)
        print(f"\n¡¡La ruleta ha salido!! {ruleta}")

        gana = False

        if eleccion == "1":
            if ruleta == numero:
                gana = True

        elif eleccion == "2": 
            if ruleta != 0 and ruleta % 2 == 0:
                gana = True

        elif eleccion == "3":
            if ruleta % 2 != 0:
                gana = True

        if gana:
            print("¡¡Has ganado!!")
            self.gestionar_apuesta(self.uid, apuesta * 2)
        else:
            print("¡¡Has perdido!!")

        print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")
