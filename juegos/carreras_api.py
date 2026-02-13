import random
from juegos.base_juegos import *

class JuegoCarrerasAPI(Juego):
    def __init__(self, usuarios, uid, gestionar_apuesta, guardar_datos):
        super().__init__("carreras", usuarios, uid, gestionar_apuesta, guardar_datos)
        
        self.caballos = {
            "1": {"nombre": "Secretariat", "prob": 40, "mult": 2},
            "2": {"nombre": "Tamamo Cross", "prob": 30, "mult": 3},
            "3": {"nombre": "Epona", "prob": 20, "mult": 4},
            "4": {"nombre": "Tormenta China", "prob": 10, "mult": 5}
        }

    def ejecutar_logica(self, apuesta, eleccion):
        if eleccion not in self.caballos:
            return {"error": "Selección de caballo no válida"}

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
        caballo_elegido = self.caballos[eleccion]["nombre"]
        
        gano = (eleccion == ganador_id)
        multiplicador = self.caballos[eleccion]["mult"] if gano else 0
        
        detalle_partida = f"Apostó por {caballo_elegido}. Ganador: {ganador_nombre}"

        self.procesar_resultado(apuesta, gano, multiplicador, detalle_partida)

        return {
            "juego": "carreras",
            "tu_caballo": caballo_elegido,
            "ganador": ganador_nombre,
            "resultado": "gano" if gano else "perdio",
            "fichas_ganadas": apuesta * multiplicador if gano else 0,
            "fichas_finales": self.usuarios[self.uid]['fichas'],
            "detalles": detalle_partida
        }