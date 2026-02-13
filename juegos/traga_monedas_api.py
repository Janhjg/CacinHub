import random
from juegos.base_juegos import *

class JuegoTragaMonedasAPI(Juego):
    def __init__(self, usuarios, uid, gestionar_apuesta, guardar_datos):
        super().__init__("tragamonedas", usuarios, uid, gestionar_apuesta, guardar_datos)

    def ejecutar_logica(self, apuesta):
        if apuesta > 10:
            return {"error": "APUESTA MUY ELEVADA", "limite": 10}

        casillas = [random.randint(0, 7) for _ in range(3)]
        casilla1, casilla2, casilla3 = casillas
        
        gana = (casilla1 == casilla2 == casilla3)
        multiplicador = 0
        detalles = ""

        if gana:
            multiplicador = (casilla1 + 2) * 10
            detalles = f"¡¡ENHORABUENA HAS GANADO!! Tres {casilla1} seguidos."
        else:
            detalles = "¡¡HAS PERDIDO LA MANUTENCION DE TUS HIJOS!!"

        self.procesar_resultado(apuesta, gana, multiplicador, detalles)

        return {
            "juego": "tragamonedas",
            "combinacion": casillas,
            "resultado": "gano" if gana else "perdio",
            "multiplicador_aplicado": multiplicador,
            "fichas_ganadas": apuesta * multiplicador if gana else 0,
            "fichas_finales": self.usuarios[self.uid]['fichas'],
            "detalles": detalles
        }