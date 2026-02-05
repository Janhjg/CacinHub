import json
import os
from datetime import datetime

HISTORIAL_PATH = "base_data/historial.json"

def cargar_json(ruta):
    if not os.path.exists(ruta):
        return {}
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def guardar_json(ruta, datos):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def registrar_partida(user_id, nombre, juego, apuesta, detalles, resultado, ganancia, antes, despues):
    historial = cargar_json(HISTORIAL_PATH)
    user_id = str(user_id)

    if user_id not in historial:
        historial[user_id] = {
            "usuario": nombre,
            "partidas": []
        }

    nueva_entrada = {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "juego": juego,
        "apuesta": apuesta,
        "detalles": detalles,
        "resultado": resultado,
        "ganancia": ganancia,
        "saldo_antes": antes,
        "saldo_despues": despues
    }

    historial[user_id]["partidas"].insert(0, nueva_entrada)
    
    historial[user_id]["partidas"] = historial[user_id]["partidas"][:50]

    guardar_json(HISTORIAL_PATH, historial)

def obtener_historial_usuario(user_id):
    historial = cargar_json(HISTORIAL_PATH)
    user_id = str(user_id)

    if user_id not in historial:
        return None

    partidas = historial[user_id]["partidas"]
    
    stats = {
        "partidas_totales": len(partidas),
        "fichas_actuales": partidas[0]["saldo_despues"] if partidas else 0
    }

    return {
        "usuario": historial[user_id]["usuario"],
        "fichas_actuales": stats["fichas_actuales"],
        "stats": stats,
        "ultimas_partidas": partidas[:5] 
    }