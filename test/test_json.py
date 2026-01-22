import json

# Ruta del archivo JSON
users_path = "./base_data/users.json"

# Fichas iniciales
fichas_iniciales = 100.0

# Función para cargar usuarios
def cargar_usuarios():
    with open(users_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("users", [])


# ----------------------------
# Tests de saldo
# ----------------------------

# Las fichas iniciales del usuario debe ser exactamente 100 fichas
def test_fichas_iniciales_correcto():

    usuarios = cargar_usuarios()
    usuario = usuarios[0]

    assert usuario["saldo"] == fichas_iniciales, (
        f"Las fichas iniciales deben ser {fichas_iniciales}"
    )

# Comprueba que un depósito positivo incrementa el saldo
def test_saldo_incrementado():

    usuarios = cargar_usuarios()
    usuario = usuarios[0]

    fichas_iniciales = usuario["saldo"]
    deposito = 50.0

    saldo_final = fichas_inicial + deposito

    assert saldo_final > fichas_iniciales
    assert saldo_final == fichas_iniciales + deposito

# No se debe permitir un depósito de 0
def test_rechazo_deposito_cero():

        deposito = 0.0

    assert deposito > 0, "No se debe permitir un depósito de 0"

# No se permiten valores negativos ni en saldo ni en depósitos
def test_no_numeros_negativos():

    usuarios = cargar_usuarios()
    usuario = usuarios[0]

    saldo = usuario["saldo"]
    deposito = -10.0

    assert saldo >= 0, "El saldo no puede ser negativo"
    assert deposito >= 0, "No se permiten depósitos negativos"