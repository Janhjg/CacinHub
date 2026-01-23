import random
from funciones import *
import json
users = "./users.json"
def get_user():
    i = 0
    while i == 0:
        id_users = print(int(input("introduzca su id para iniciar el juego: ")))
        for id in users["id"]:
            if id_users != users["id"]:
                return f"este usuario no es valido, porfavor introduzca otro id: {id_users}"
            else:
                i += 1

def apuesta(id_user):
    id_user = get_user()
    inicio_de_apuesto = print(int(input("Indique que apuesta quiere hacer, 1 para apostar un numero, 2 para numero mayor y 3 para numero menor: ")))
    while inicio_de_apuesto >= 1 or inicio_de_apuesto <= 3:
        if inicio_de_apuesto == 1:
            apostar_numero = print(int(input("Indique a que numero al que apuesta: ")))
            return apostar_numero
        elif inicio_de_apuesto == 2:
            apostar_mayor = print("Ha elegido apuesta a que su numero es mayor")
            return apostar_mayor
        elif inicio_de_apuesto == 3:
            apostar_menor = print("Ha elegido apuesta a que su numero es menor")
            return apostar_menor

    apuesta = print(int(input("Indique apuesta a realizar: ")))
    if apuesta >= 1:
        pass