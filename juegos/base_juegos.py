import time
import random
from Funciones.historial import registrar_partida

class Juego:
    def __init__(self, nombre_juego, usuarios, uid, gestionar_apuesta, guardar_datos):
        self.nombre_juego = nombre_juego
        self.usuarios = usuarios
        self.uid = str(uid)
        self.gestionar_apuesta = gestionar_apuesta
        self.guardar_datos = guardar_datos

    def solicitar_apuesta(self):
        try:
            if self.uid not in self.usuarios:
                print(f"Error: Usuario {self.uid} no encontrado.")
                return None

            fichas_actuales = self.usuarios[self.uid]["fichas"]
            print(f"\nSaldo disponible: {fichas_actuales} fichas")
            
            entrada = input(f"Cuanto deseas apostar en {self.nombre_juego}: ")
            monto = int(entrada)

            if monto <= 0:
                print("La apuesta debe ser mayor a 0.")
                return None
            
            if monto > fichas_actuales:
                print("No tienes suficientes fichas para esta apuesta.")
                return None

            return monto
        except ValueError:
            print("Error: Debes ingresar un numero entero valido.")
            return None

    def procesar_resultado(self, apuesta, gano, multiplicador, detalles="Sin detalles"):
        fichas_antes = self.usuarios[self.uid]["fichas"] # Saldo real antes de la jugada
        
        self.usuarios = self.gestionar_apuesta(
            self.usuarios, self.uid, apuesta, self.nombre_juego, gano, multiplicador
        )
        
        fichas_despues = self.usuarios[self.uid]["fichas"]

        if gano:
            if multiplicador == 1:
                resultado_txt = "empate"
                valor_historial = 0
            else:
                resultado_txt = "gano"
                valor_historial = fichas_despues - fichas_antes
        else:
            resultado_txt = "perdio"
            valor_historial = apuesta 

        registrar_partida(
            self.uid, self.usuarios[self.uid]["nombre"], self.nombre_juego, 
            apuesta, detalles, resultado_txt, valor_historial, fichas_antes, fichas_despues
        )
        
        self.guardar_datos(self.usuarios)
        return self.usuarios
        
        return self.usuarios

    def animacion_espera(self, mensaje=""):
        if mensaje:
            print(f"\n{mensaje}")
        for _ in range(3):
            print("... ", end="", flush=True)
            time.sleep(0.6)
        print("\n")