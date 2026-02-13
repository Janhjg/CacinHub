from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from Funciones.historial import cargar_json, guardar_json, obtener_historial_usuario
from Funciones.funciones import gestionar_apuesta

from juegos.dados_api import JuegoDadosAPI
from juegos.carreras_api import JuegoCarrerasAPI
from juegos.ruleta_api import JuegoRuletaAPI
from juegos.traga_monedas_api import JuegoTragaMonedasAPI

app = FastAPI(title="Casino CancinHub API", description="API profesional para el Casino Virtual")

DB_PATH = "base_data/users.json"

class DatosApuesta(BaseModel):
    user_id: str
    monto: int
    eleccion: Optional[str] = "1"

class DatosApuestaRuleta(BaseModel):
    user_id: str
    monto: int
    tipo_apuesta: str  # "1": Pleno, "2": Rojo, "3": Negro
    numero: Optional[int] = None

"""--- ENDPOINTS DE JUEGOS ---"""

@app.post("/jugar/dados")
def api_dados(req: DatosApuesta):
    usuarios = cargar_json(DB_PATH)
    if req.user_id not in usuarios:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if req.monto > usuarios[req.user_id]["fichas"]:
        raise HTTPException(status_code=400, detail="Fichas insuficientes")

    juego = JuegoDadosAPI(usuarios, req.user_id, gestionar_apuesta, lambda d: guardar_json(DB_PATH, d))
    return juego.ejecutar_logica(req.monto)

@app.post("/jugar/carreras")
def api_carreras(req: DatosApuesta):
    usuarios = cargar_json(DB_PATH)
    if req.user_id not in usuarios:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    juego = JuegoCarrerasAPI(usuarios, req.user_id, gestionar_apuesta, lambda d: guardar_json(DB_PATH, d))
    if req.eleccion not in juego.caballos:
        raise HTTPException(status_code=400, detail="Ese caballo no existe en el hipódromo")

    return juego.ejecutar_logica(req.monto, req.eleccion)

@app.post("/jugar/ruleta")
def api_ruleta(req: DatosApuestaRuleta):
    usuarios = cargar_json(DB_PATH)
    if req.user_id not in usuarios:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if req.monto > usuarios[req.user_id]["fichas"]:
        raise HTTPException(status_code=400, detail="Fichas insuficientes")

    juego = JuegoRuletaAPI(usuarios, req.user_id, gestionar_apuesta, lambda d: guardar_json(DB_PATH, d))
    
    if req.tipo_apuesta == "1" and (req.numero is None or req.numero < 0 or req.numero > 36):
        raise HTTPException(status_code=400, detail="Para apuesta tipo 1, elige un número entre 0 y 36")

    return juego.ejecutar_logica(req.monto, req.tipo_apuesta, req.numero)

@app.post("/jugar/tragamonedas")
def api_tragamonedas(req: DatosApuesta):
    usuarios = cargar_json(DB_PATH)
    if req.user_id not in usuarios:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if req.monto > usuarios[req.user_id]["fichas"]:
        raise HTTPException(status_code=400, detail="Fichas insuficientes")

    juego = JuegoTragaMonedasAPI(usuarios, req.user_id, gestionar_apuesta, lambda d: guardar_json(DB_PATH, d))
    resultado = juego.ejecutar_logica(req.monto)
    
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
        
    return resultado