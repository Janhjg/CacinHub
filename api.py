from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
import json
import os

# Importaciones de módulos de lógica
from Funciones.historial import cargar_json, guardar_json, obtener_historial_usuario, registrar_partida
from Funciones.funciones import gestionar_apuesta, Usuario, calcular_edad
from Funciones.gacha import GachaChistes

# Importaciones de los juegos (Versión API)
from juegos.dados_api import JuegoDadosAPI
from juegos.carreras_api import JuegoCarrerasAPI
from juegos.ruleta_api import JuegoRuletaAPI
from juegos.traga_monedas_api import JuegoTragaMonedasAPI

app = FastAPI(
    title="Casino CancinHub API", 
    description="Backend profesional para el Casino Virtual. ¡Zawa Zawa!",
    version="2.0.0"
)

# RUTAS DE ARCHIVOS
DB_PATH = "base_data/users.json"
DB_PATH_HISTORIAL = "base_data/historial.json"

# --- MODELOS DE DATOS (PYDANTIC) ---

class DatosApuesta(BaseModel):
    user_id: str
    monto: int
    eleccion: Optional[str] = "1"

class DatosApuestaRuleta(BaseModel):
    user_id: str
    monto: int
    tipo_apuesta: str  # "1": Pleno, "2": Rojo, "3": Negro
    numero: Optional[int] = None

class CrearUsuarioRequest(BaseModel):
    nombre: str
    contrasena: str
    fecha_nacimiento: str

class AgregarFichasRequest(BaseModel):
    user_id: str
    contrasena: str
    cantidad: int

# --- FUNCIONES DE UTILIDAD INTERNA ---

def cargar_db_usuarios():
    return cargar_json(DB_PATH)

def guardar_db_usuarios(datos):
    guardar_json(DB_PATH, datos)

def cargar_db_historial():
    return cargar_json(DB_PATH_HISTORIAL)

# --- ENDPOINTS DE GESTIÓN DE USUARIOS ---

@app.post("/api/usuarios", status_code=201)
def crear_usuario_endpoint(req: CrearUsuarioRequest):
    """Crea un nuevo usuario con validación de edad y nombre."""
    if len(req.nombre.strip()) < 3:
        raise HTTPException(status_code=400, detail="El nombre debe tener al menos 3 caracteres")
    
    if len(req.contrasena) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")
    
    edad = calcular_edad(req.fecha_nacimiento)
    if edad is None:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use DD/MM/YYYY")
    
    if edad < 18:
        raise HTTPException(status_code=403, detail=f"Acceso denegado: Tienes {edad} años. Solo mayores de 18.")

    usuarios_db = cargar_db_usuarios()
    
    nuevo_user = Usuario(req.nombre.strip(), req.contrasena, req.fecha_nacimiento.strip())
    
    if nuevo_user.id in usuarios_db:
        raise HTTPException(status_code=409, detail="El ID de usuario ya existe. Intenta con un nombre diferente.")

    usuarios_db[nuevo_user.id] = nuevo_user.to_dict()
    guardar_db_usuarios(usuarios_db)
    
    return {"success": True, "message": "Usuario creado", "data": nuevo_user.to_dict()}

@app.get("/api/usuarios/{user_id}/info")
def obtener_info_usuario(user_id: str, contrasena: str):
    usuarios = cargar_db_usuarios()
    if user_id not in usuarios or usuarios[user_id]["contrasena"] != contrasena:
        raise HTTPException(status_code=401, detail="ID o contraseña incorrectos")
    
    return {"success": True, "data": usuarios[user_id]}

# --- ENDPOINTS DE JUEGOS ---

@app.post("/jugar/dados")
def api_dados(req: DatosApuesta):
    usuarios = cargar_db_usuarios()
    if req.user_id not in usuarios: raise HTTPException(404, "Usuario no encontrado")
    if req.monto > usuarios[req.user_id]["fichas"]: raise HTTPException(400, "Fichas insuficientes")

    juego = JuegoDadosAPI(usuarios, req.user_id, gestionar_apuesta, guardar_db_usuarios)
    return juego.ejecutar_logica(req.monto)

@app.post("/jugar/tragamonedas")
def api_tragamonedas(req: DatosApuesta):
    usuarios = cargar_db_usuarios()
    if req.user_id not in usuarios: raise HTTPException(404, "Usuario no encontrado")
    if req.monto > usuarios[req.user_id]["fichas"]: raise HTTPException(400, "Fichas insuficientes")
    if req.monto > 10: raise HTTPException(400, "Apuesta máxima permitida: 10")

    juego = JuegoTragaMonedasAPI(usuarios, req.user_id, gestionar_apuesta, guardar_db_usuarios)
    return juego.ejecutar_logica(req.monto)

@app.post("/jugar/carreras")
def api_carreras(req: DatosApuesta):
    usuarios = cargar_db_usuarios()
    if req.user_id not in usuarios: raise HTTPException(404)
    if req.monto > usuarios[req.user_id]["fichas"]: raise HTTPException(400, "Fichas insuficientes")
    
    juego = JuegoCarrerasAPI(usuarios, req.user_id, gestionar_apuesta, guardar_db_usuarios)
    if req.eleccion not in juego.caballos:
        raise HTTPException(400, detail="Ese caballo no existe")

    return juego.ejecutar_logica(req.monto, req.eleccion)

@app.post("/jugar/ruleta")
def api_ruleta(req: DatosApuestaRuleta):
    usuarios = cargar_db_usuarios()
    if req.user_id not in usuarios: raise HTTPException(404, "Usuario no encontrado")
    if req.monto > usuarios[req.user_id]["fichas"]: raise HTTPException(400, "Fichas insuficientes")

    juego = JuegoRuletaAPI(usuarios, req.user_id, gestionar_apuesta, guardar_db_usuarios)
    if req.tipo_apuesta not in ["1", "2", "3"]:
        raise HTTPException(400, detail="Tipo de apuesta inválido")
    
    return juego.ejecutar_logica(req.monto, req.tipo_apuesta, req.numero)

@app.post("/gacha/chiste")
def api_tirar_gacha(user_id: str):
    usuarios = cargar_db_usuarios()
    if user_id not in usuarios: raise HTTPException(404, "Usuario no encontrado")
    
    gacha = GachaChistes(usuarios, user_id, guardar_db_usuarios)
    resultado = gacha.tirar_gacha()
    
    if "error" in resultado: raise HTTPException(400, detail=resultado["error"])
    return resultado

# --- ENDPOINTS DE HISTORIAL Y BANCO ---

@app.get("/jugadas/fecha")
def get_jugadas_por_fecha(fecha: str = Query(..., description="DD/MM/YYYY")):
    datos_historial = cargar_db_historial()
    resultado = []

    for uid, info in datos_historial.items():
        filtradas = [p for p in info["partidas"] if p["fecha"].startswith(fecha)]
        if filtradas:
            resultado.append({"id": uid, "usuario": info["usuario"], "partidas": filtradas})

    if not resultado: raise HTTPException(404, detail="Sin registros en esa fecha")
    return resultado

@app.post("/api/banco/agregar-fichas")
def agregar_fichas_banco(req: AgregarFichasRequest):
    usuarios = cargar_db_usuarios()
    if req.user_id not in usuarios or usuarios[req.user_id]["contrasena"] != req.contrasena:
        raise HTTPException(401, "Credenciales inválidas")
    
    if req.cantidad <= 0: raise HTTPException(400, "La cantidad debe ser positiva")
    
    fichas_antes = usuarios[req.user_id]["fichas"]
    usuarios[req.user_id]["fichas"] += req.cantidad
    
    registrar_partida(
        user_id=req.user_id,
        nombre=usuarios[req.user_id]["nombre"],
        juego="banco",
        apuesta=0,
        detalles="Ingreso desde API Banco",
        resultado="gano",
        ganancia=req.cantidad,
        antes=fichas_antes,
        despues=usuarios[req.user_id]["fichas"]
    )
    
    guardar_db_usuarios(usuarios)
    return {"success": True, "fichas_actuales": usuarios[req.user_id]["fichas"]}

# --- ENDPOINTS DE HISTÓRICO ---

@app.get("/jugadas")
def get_todos_los_usuarios():
    """
    Obtiene el historial completo de todos los usuarios registrados 
    en el archivo historial.json.
    """
    try:
        datos = cargar_db_historial()
        
        resultado = []
        for user_id, info in datos.items():
            resultado.append({
                "id": user_id,
                "usuario": info["usuario"],
                "total_partidas": len(info.get("partidas", [])),
                "partidas": info.get("partidas", [])
            })
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el historial: {str(e)}")

@app.get("/jugadas/{user_id}")
def get_jugadas_usuario(user_id: str):
    """
    Obtiene todas las jugadas de un usuario específico por su ID.
    """
    datos = cargar_db_historial()
    
    if user_id not in datos:
        raise HTTPException(
            status_code=404, 
            detail=f"Historial para el usuario con ID {user_id} no encontrado"
        )
    
    usuario_data = datos[user_id]
    
    return {
        "id": user_id,
        "usuario": usuario_data["usuario"],
        "total_partidas": len(usuario_data.get("partidas", [])),
        "partidas": usuario_data.get("partidas", [])
    }

@app.get("/api/usuarios")
def listar_usuarios():
    """
    Lista todos los usuarios creados en el sistema (solo ID y nombre).
    Utiliza el archivo users.json.
    """
    usuarios_db = cargar_db_usuarios()
    
    usuarios_lista = []
    for user_id, usuario in usuarios_db.items():
        usuarios_lista.append({
            "id": user_id,
            "nombre": usuario["nombre"]
        })
    
    return {
        "success": True,
        "count": len(usuarios_lista),
        "data": usuarios_lista
    }