import random
from juegos.base_juegos import *

class JuegoTraga_monedas(Juego):
    def __init__(self, usuarios, uid, gestionar_apuesta, guardar_datos):
        super().__init__("dados", usuarios, uid, gestionar_apuesta, guardar_datos)
        

    def jugar(self):
        print("\n" + "="*35)
        print("--- LA ROBA SUELDOS ---")
        print("="*35)
        
        apuesta = self.solicitar_apuesta()
        casilla1 = random.randint(0, 7)
        casilla2 = random.randint(0, 7)
        casilla3 = random.randint(0, 7)
        main = [casilla1, casilla2, casilla3]
        if apuesta <= 10:
            print (main)
            if casilla1 == casilla2 == casilla3:
                if casilla1 == 0:
                    print("¡¡ENHORABUENA HAS GANADO!!")
                    self.procesar_resultado(apuesta, True, 20)
                    print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")

                elif casilla1 == 1:
                    print("¡¡ENHORABUENA HAS GANADO!!")
                    self.procesar_resultado(apuesta, True, 30)
                    print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")    

                elif casilla1 == 2:
                    print("¡¡ENHORABUENA HAS GANADO!!")
                    self.procesar_resultado(apuesta, True, 40)
                    print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")

                elif casilla1 == 3:
                    print("¡¡ENHORABUENA HAS GANADO!!")
                    self.procesar_resultado(apuesta, True, 50)
                    print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")   

                elif casilla1 == 4:
                    print("¡¡ENHORABUENA HAS GANADO!!")
                    self.procesar_resultado(apuesta, True, 60)
                    print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")

                elif casilla1 == 5:
                    print("¡¡ENHORABUENA HAS GANADO!!")
                    self.procesar_resultado(apuesta, True, 70)
                    print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")

                elif casilla1 == 6:
                    print("¡¡ENHORABUENA HAS GANADO!!")
                    self.procesar_resultado(apuesta, True, 80)
                    print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")

                elif casilla1 == 7:
                    print("¡¡ENHORABUENA HAS GANADO!!")
                    self.procesar_resultado(apuesta, True, 90)
                    print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")
            else:
                print("¡¡HAS PERDIDO MANUTENCION DE TUS HIJOS!!")
                self.procesar_resultado(apuesta, False, 0)
                print(f"\nSaldo actual: {self.usuarios[self.uid]['fichas']} fichas.")
        else:
            print("APUESTA MUY ELEVADA")
            return