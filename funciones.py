# =========================
# LIBRERIAS
# =========================

import random, time, os, json

# =========================
# USUARIOS
# =========================

class Usuario:
    def __init__(self, nombre: str, password: str):
        pass

    def verificar_password(self, password: str) -> bool:
        pass

    def sumar_creditos(self, cantidad: int):
        pass

    def restar_creditos(self, cantidad: int) -> bool:
        pass

    def obtener_creditos(self) -> int:
        pass


class GestorUsuarios:
    def __init__(self):
        pass

    def crear_usuario(self, nombre: str, password: str) -> bool:
        pass

    def iniciar_sesion(self, nombre: str, password: str) -> Usuario | None:
        pass

    def guardar_usuarios(self):
        pass

    def cargar_usuarios(self):
        pass


# =========================
# TIENDA / GACHA DE CHISTES
# =========================

def tienda_chistes(usuario: Usuario):
    pass

def obtener_chiste_aleatorio():
    pass


# =========================
# JUEGOS
# =========================

def juego_ruleta(usuario: Usuario):
    pass

def juego_tragaperras(usuario: Usuario):
    pass

def juego_carrera_caballos(usuario: Usuario):
    pass

def juego_blackjack(usuario: Usuario):
    pass


# =========================
# PERSISTENCIA JSON
# =========================

def guardar_datos():
    pass

def cargar_datos():
    pass


# =========================
# MENÚS
# =========================

def menu_principal(usuario: Usuario):
    pass

def menu_login():
    pass


# =========================
# MAIN
# =========================

def main():
    pass


if __name__ == "__main__":
    main()