from Funciones.funciones import iniciar_sesion
from Funciones.historial import registrar_partida
from datetime import datetime

def ejecutar_banco(usuarios, uid_actual, guardar_callback):
    print("\n" + "="*35)
    print("       SISTEMA BANCARIO CENTRAL")
    print("="*35)
    print("Por seguridad, confirme su identidad.")
    
    confirm_uid = input("ID de usuario: ")
    confirm_pass = input("Contrasena: ")

    if confirm_uid == str(uid_actual) and iniciar_sesion(usuarios, confirm_uid, confirm_pass):
        try:
            fichas_antes = usuarios[uid_actual]['fichas']
            print(f"\nAutenticacion exitosa.")
            print(f"Saldo actual: {fichas_antes} fichas.")
            
            cantidad = int(input("Ingrese la cantidad de fichas a obtener: "))
            
            if cantidad > 0:
                usuarios[uid_actual]['fichas'] += cantidad
                fichas_despues = usuarios[uid_actual]['fichas']
                
                registrar_partida(
                    user_id=uid_actual,
                    nombre=usuarios[uid_actual]['nombre'],
                    juego="banco",
                    apuesta=0, 
                    detalles=f"Retiro de fondos bancarios",
                    resultado="gano", 
                    ganancia=cantidad,
                    antes=fichas_antes,
                    despues=fichas_despues
                )
                
                guardar_callback(usuarios)
                
                print(f"Operacion exitosa. Ahora tienes {fichas_despues} fichas.")
            else:
                print("Error: La cantidad debe ser mayor a 0.")
                
        except ValueError:
            print("Error: Ingrese un numero entero valido.")
    else:
        print("Error de autenticacion: ID o contrasena incorrectos.")
