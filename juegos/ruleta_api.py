import random
from juegos.base_juegos import *

class JuegoRuletaAPI(Juego):
    def init(self, usuarios, uid, gestionar_apuesta, guardar_datos):
        super().init("ruleta", usuarios, uid, gestionar_apuesta, guardar_datos)
        self.numeros = list(range(0, 37))

    def ejecutar_logica(self, apuesta, tipo_apuesta, numero_elegido=None):
        ruleta = random.randint(0, 36)
        gana = False
        multiplicador = 0
        detalles = ""

        if tipo_apuesta == "1":
            if numero_elegido is not None and int(numero_elegido) == ruleta:
                gana = True
                multiplicador = 36 
            detalles = f"Apostó al número {numero_elegido}. Salió el {ruleta}."

        elif tipo_apuesta == "2":
            if ruleta != 0 and ruleta % 2 == 0:
                gana = True
                multiplicador = 2
            detalles = f"Apostó a Rojo (Pares). Salió el {ruleta}."

        elif tipo_apuesta == "3":
            if ruleta % 2 != 0:
                gana = True
                multiplicador = 2
            detalles = f"Apostó a Negro (Impares). Salió el {ruleta}."

        self.procesar_resultado(apuesta, gana, multiplicador, detalles)

        return {
            "juego": "ruleta",
            "tipo_apuesta": tipo_apuesta,
            "numero_ganador": ruleta,
            "resultado": "gano" if gana else "perdio",
            "fichas_ganadas": apuesta * multiplicador if gana else 0,
            "fichas_finales": self.usuarios[self.uid]['fichas'],
            "detalles": detalles
        }