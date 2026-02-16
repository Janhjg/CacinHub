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

@app.get("/api/historial/{user_id}")
def obtener_historial_completo(user_id: str, contrasena: str, limite: int = 10):
    # Cargar usuarios
    usuarios = cargar_json(DB_PATH)
    
    # Verificar que el usuario existe
    if user_id not in usuarios:
        return {"success": False, "message": "Usuario no encontrado"}
    
    # Verificar contraseña
    if usuarios[user_id]["contrasena"] != contrasena:
        return {"success": False, "message": "Contraseña incorrecta"}
    
    # Cargar historial
    historial = cargar_json("base_data/historial.json")
    
    # Si el usuario no tiene historial
    if user_id not in historial:
        return {
            "success": True,
            "message": "Usuario sin historial",
            "data": {"usuario": "", "total_partidas": 0, "partidas": []}
        }
    
    # Obtener partidas del usuario
    usuario_hist = historial[user_id]
    partidas = usuario_hist["partidas"]
    
    # Limitar cantidad de partidas
    if limite > 0:
        partidas = partidas[:limite]
    
    # Calcular estadisticas
    ganadas = 0
    perdidas = 0
    total_ganado = 0
    total_perdido = 0
    
    for partida in historial[user_id]["partidas"]:
        if partida["resultado"] == "gano":
            ganadas = ganadas + 1
            total_ganado = total_ganado + partida["ganancia"]
        elif partida["resultado"] == "perdio":
            perdidas = perdidas + 1
            total_perdido = total_perdido + partida["apuesta"]
    
    balance = total_ganado - total_perdido
    
    return {
        "success": True,
        "message": "Historial obtenido",
        "data": {
            "usuario": usuario_hist["usuario"],
            "total_partidas": len(historial[user_id]["partidas"]),
            "estadisticas": {
                "partidas_ganadas": ganadas,
                "partidas_perdidas": perdidas,
                "total_ganado": total_ganado,
                "total_perdido": total_perdido,
                "balance": balance
            },
            "partidas": partidas
        }
    }


@app.get("/api/historial/{user_id}/juego/{nombre_juego}")
def obtener_historial_por_juego(user_id: str, nombre_juego: str, contrasena: str, limite: int = 10):
    # Cargar usuarios
    usuarios = cargar_json(DB_PATH)
    
    # Verificar usuario
    if user_id not in usuarios:
        return {"success": False, "message": "Usuario no encontrado"}
    
    # Verificar contraseña
    if usuarios[user_id]["contrasena"] != contrasena:
        return {"success": False, "message": "Contraseña incorrecta"}
    
    # Cargar historial
    historial = cargar_json("base_data/historial.json")
    
    if user_id not in historial:
        return {
            "success": True,
            "message": "Usuario sin historial",
            "data": {"usuario": "", "juego": nombre_juego, "total_partidas": 0, "partidas": []}
        }
    
    usuario_hist = historial[user_id]
    todas_partidas = usuario_hist["partidas"]
    
    # Filtrar solo las partidas del juego que queremos
    partidas_juego = []
    for partida in todas_partidas:
        if partida["juego"].lower() == nombre_juego.lower():
            partidas_juego.append(partida)
    
    # Aplicar limite
    if limite > 0:
        partidas_juego = partidas_juego[:limite]
    
    # Calcular estadisticas del juego
    ganadas = 0
    perdidas = 0
    total_ganado = 0
    total_perdido = 0
    
    for partida in partidas_juego:
        if partida["resultado"] == "gano":
            ganadas = ganadas + 1
            total_ganado = total_ganado + partida["ganancia"]
        elif partida["resultado"] == "perdio":
            perdidas = perdidas + 1
            total_perdido = total_perdido + partida["apuesta"]
    
    return {
        "success": True,
        "message": "Historial de " + nombre_juego + " obtenido",
        "data": {
            "usuario": usuario_hist["usuario"],
            "juego": nombre_juego,
            "total_partidas": len(partidas_juego),
            "estadisticas": {
                "partidas_ganadas": ganadas,
                "partidas_perdidas": perdidas,
                "total_ganado": total_ganado,
                "total_perdido": total_perdido,
                "balance": total_ganado - total_perdido
            },
            "partidas": partidas_juego
        }
    }


@app.get("/api/historial/{user_id}/estadisticas")
def obtener_estadisticas_usuario(user_id: str, contrasena: str):
    # Cargar usuarios
    usuarios = cargar_json(DB_PATH)
    
    if user_id not in usuarios:
        return {"success": False, "message": "Usuario no encontrado"}
    
    if usuarios[user_id]["contrasena"] != contrasena:
        return {"success": False, "message": "Contraseña incorrecta"}
    
    usuario = usuarios[user_id]
    
    # Cargar historial
    historial = cargar_json("base_data/historial.json")
    
    if user_id not in historial:
        return {
            "success": True,
            "data": {
                "usuario": usuario["nombre"],
                "fichas_actuales": usuario["fichas"],
                "estadisticas": {
                    "total_partidas": 0,
                    "partidas_ganadas": 0,
                    "partidas_perdidas": 0,
                    "total_ganado": 0,
                    "balance_total": 0,
                    "juego_favorito": "ninguno"
                }
            }
        }
    
    usuario_hist = historial[user_id]
    partidas = usuario_hist["partidas"]
    
    # Calcular estadisticas
    total_partidas = len(partidas)
    ganadas = 0
    perdidas = 0
    total_ganado = 0
    total_perdido = 0
    
    for partida in partidas:
        if partida["resultado"] == "gano":
            ganadas = ganadas + 1
            total_ganado = total_ganado + partida["ganancia"]
        elif partida["resultado"] == "perdio":
            perdidas = perdidas + 1
            total_perdido = total_perdido + partida["apuesta"]
    
    # Calcular juego favorito
    juegos = {}
    for partida in partidas:
        juego = partida["juego"]
        if juego in juegos:
            juegos[juego] = juegos[juego] + 1
        else:
            juegos[juego] = 1
    
    # Encontrar el juego con mas partidas
    juego_favorito = "ninguno"
    max_partidas = 0
    for juego in juegos:
        if juegos[juego] > max_partidas:
            max_partidas = juegos[juego]
            juego_favorito = juego
    
    # Calcular tasa de victoria
    if total_partidas > 0:
        tasa_victoria = (ganadas / total_partidas) * 100
        tasa_victoria = round(tasa_victoria, 2)
    else:
        tasa_victoria = 0
    
    # Ver racha actual (ultimas 5 partidas)
    ultimas_5 = partidas[:5]
    racha = "ninguna"
    
    if len(ultimas_5) > 0:
        todas_ganadas = True
        todas_perdidas = True
        
        for partida in ultimas_5:
            if partida["resultado"] != "gano":
                todas_ganadas = False
            if partida["resultado"] != "perdio":
                todas_perdidas = False
        
        if todas_ganadas:
            racha = "Racha ganadora (" + str(len(ultimas_5)) + " victorias)"
        elif todas_perdidas:
            racha = "Racha perdedora (" + str(len(ultimas_5)) + " derrotas)"
        else:
            racha = "Mixta"
    
    return {
        "success": True,
        "message": "Estadisticas obtenidas",
        "data": {
            "usuario": usuario_hist["usuario"],
            "fichas_actuales": usuario["fichas"],
            "estadisticas": {
                "total_partidas": total_partidas,
                "partidas_ganadas": ganadas,
                "partidas_perdidas": perdidas,
                "tasa_victoria": tasa_victoria,
                "total_ganado": total_ganado,
                "balance_total": total_ganado - total_perdido,
                "juego_favorito": juego_favorito,
                "racha_actual": racha
            }
        }
    }