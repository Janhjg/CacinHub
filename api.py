from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import json

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
    if req.monto > usuarios[req.user_id]["fichas"]:
        raise HTTPException(status_code=400, detail="Fichas insuficientes")
        
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

# ===========================================
# ENDPOINT CREAR USUARIO
# ==========================================
from Funciones.funciones import Usuario, calcular_edad

class CrearUsuarioRequest(BaseModel):
    nombre: str
    contrasena: str
    fecha_nacimiento: str

def cargar_usuarios():
    """Carga usuarios desde JSON"""
    archivo = "base_data/users.json"
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_usuarios(usuarios_db):
    """Guarda usuarios en JSON"""
    archivo = "base_data/users.json"
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(usuarios_db, f, indent=4, ensure_ascii=False)




@app.post("/api/usuarios")
def crear_usuario_endpoint(usuario: CrearUsuarioRequest):
    """Crear un nuevo usuario"""
    
    # Validaciones
    if len(usuario.nombre.strip()) < 3:
        return {
            "success": False,
            "message": "El nombre debe tener al menos 3 caracteres",
            "data": None
        }
    
    if len(usuario.contrasena) < 6:
        return {
            "success": False,
            "message": "La contraseña debe tener al menos 6 caracteres",
            "data": None
        }
    
    # Validar edad
    edad = calcular_edad(usuario.fecha_nacimiento)
    
    if edad is None:
        return {
            "success": False,
            "message": "Formato de fecha no válido. Use DD/MM/YYYY",
            "data": None
        }
    
    if edad < 18:
        return {
            "success": False,
            "message": f"Acceso denegado: Tienes {edad} años. Solo mayores de 18.",
            "data": None
        }
    
    # Cargar usuarios
    usuarios_db = cargar_usuarios()
    
    # Crear usuario usando la clase original
    while True:
        nuevo_user = Usuario(
            usuario.nombre.strip(),
            usuario.contrasena,
            usuario.fecha_nacimiento.strip()
        )
        if nuevo_user.id not in usuarios_db:
            break
    
    # Guardar
    usuarios_db[nuevo_user.id] = nuevo_user.to_dict()
    guardar_usuarios(usuarios_db)
    
    # Respuesta
    return {
        "success": True,
        "message": "Usuario creado exitosamente",
        "data": {
            "id": nuevo_user.id,
            "nombre": nuevo_user.nombre,
            "edad": edad,
            "fichas": nuevo_user.fichas,
            "fecha_nacimiento": nuevo_user.fecha_nacimiento,
            "fecha_registro": nuevo_user.fecha_registro
        }
    }
    
@app.get("/api/usuarios")
def listar_usuarios():
    """Obtener todos los usuarios (solo id y nombre)"""
    
    usuarios_db = cargar_usuarios()
    
    # Extraer solo id y nombre
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


# =====================================================
# ENDPOINT: OBTENER SALDO
# =====================================================
class AgregarFichasRequest(BaseModel):
    user_id: str
    contrasena: str
    cantidad: int
    
@app.get("/api/usuarios/{user_id}/saldo")
def obtener_saldo(user_id: str, contrasena: str):

    usuarios = cargar_usuarios()
    
    # Verificar que el usuario existe
    if user_id not in usuarios:
        return {
            "success": False,
            "message": "Usuario no encontrado",
            "data": None
        }
    
    # Verificar contraseña
    if usuarios[user_id]["contrasena"] != contrasena:
        return {
            "success": False,
            "message": "Contraseña incorrecta",
            "data": None
        }
    
    usuario = usuarios[user_id]
    
    # Retornar saldo
    return {
        "success": True,
        "message": "Saldo obtenido exitosamente",
        "data": {
            "user_id": user_id,
            "nombre": usuario["nombre"],
            "fichas": usuario["fichas"]
        }
    }


@app.get("/api/usuarios/{user_id}/info")
def obtener_info_completa(user_id: str, contrasena: str):
    usuarios = cargar_usuarios()
    
    # Verificar que el usuario existe
    if user_id not in usuarios:
        return {
            "success": False,
            "message": "Usuario no encontrado",
            "data": None
        }
    
    # Verificar contraseña
    if usuarios[user_id]["contrasena"] != contrasena:
        return {
            "success": False,
            "message": "Contraseña incorrecta",
            "data": None
        }
    
    usuario = usuarios[user_id]
    
    # Retornar información completa
    return {
        "success": True,
        "message": "Información obtenida exitosamente",
        "data": {
            "user_id": user_id,
            "nombre": usuario["nombre"],
            "fichas": usuario["fichas"],
            "fecha_nacimiento": usuario.get("fecha_nacimiento", ""),
            "fecha_registro": usuario.get("fecha_registro", ""),
            "stats": usuario.get("stats", {})
        }
    }

@app.post("/api/banco/agregar-fichas")
def agregar_fichas_banco(request: AgregarFichasRequest):
    
    usuarios = cargar_usuarios()
    
    # Verificar que el usuario existe
    if request.user_id not in usuarios:
        return {
            "success": False,
            "message": "Usuario no encontrado",
            "data": None
        }
    
    # Verificar contraseña
    if usuarios[request.user_id]["contrasena"] != request.contrasena:
        return {
            "success": False,
            "message": "Contraseña incorrecta",
            "data": None
        }
    
    # Validar cantidad
    if request.cantidad <= 0:
        return {
            "success": False,
            "message": "La cantidad debe ser mayor a 0",
            "data": None
        }
    
    # Guardar fichas antes
    fichas_antes = usuarios[request.user_id]["fichas"]
    
    # Agregar fichas
    usuarios[request.user_id]["fichas"] += request.cantidad
    fichas_despues = usuarios[request.user_id]["fichas"]
    
    # Registrar en historial
    from Funciones.historial import registrar_partida
    
    registrar_partida(
        user_id=request.user_id,
        nombre=usuarios[request.user_id]["nombre"],
        juego="banco",
        apuesta=0,
        detalles="Retiro de fondos bancarios",
        resultado="gano",
        ganancia=request.cantidad,
        antes=fichas_antes,
        despues=fichas_despues
    )
    
    # Guardar usuarios
    guardar_usuarios(usuarios)
    
    # Respuesta exitosa
    return {
        "success": True,
        "message": f"Operación exitosa. Ahora tienes {fichas_despues} fichas",
        "data": {
            "user_id": request.user_id,
            "nombre": usuarios[request.user_id]["nombre"],
            "fichas_antes": fichas_antes,
            "fichas_agregadas": request.cantidad,
            "fichas_despues": fichas_despues
        }
    }
