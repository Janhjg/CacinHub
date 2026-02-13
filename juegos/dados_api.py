import random
from juegos.base_juegos import *

class JuegoDadosAPI(Juego):
    def __init__(self, usuarios, uid, gestionar_apuesta, guardar_datos):
        super().__init__("dados", usuarios, uid, gestionar_apuesta, guardar_datos)

    def ejecutar_logica(self, apuesta):
        tiro_jugador = random.randint(1, 6)
        tiro_banca = random.randint(1, 6)
        
        detalle_duelo = f"Jugador: {tiro_jugador} vs Banca: {tiro_banca}"

        if tiro_jugador > tiro_banca:
            resultado_texto = "gano"
            gano_bool = True
            multiplicador = 2
        elif tiro_banca > tiro_jugador:
            resultado_texto = "perdio"
            gano_bool = False
            multiplicador = 0
        else:
            resultado_texto = "empate"
            gano_bool = True
            multiplicador = 1

        self.procesar_resultado(apuesta, gano_bool, multiplicador, detalle_duelo)

        return {
            "juego": "dados",
            "tiro_jugador": tiro_jugador,
            "tiro_banca": tiro_banca,
            "resultado": resultado_texto,
            "fichas_finales": self.usuarios[self.uid]['fichas'],
            "detalles": detalle_duelo
        }