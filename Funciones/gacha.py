import random

class GachaChistes:
    def __init__(self, usuarios, uid, guardar_datos):
        self.usuarios = usuarios
        self.uid = str(uid)
        self.guardar_datos = guardar_datos
        self.costo = 5  # Coste por chiste
        
        self.lista_chistes = [
            "¿Qué hace una abeja en el gimnasio? ¡Zumba!",
            "¿Cómo se dice pañuelo en japonés? Saka-moko.",
            "¿Qué le dice un jaguar a otro jaguar? Jaguar you?",
            "¿Cómo se queda un mago después de comer? Magordi.",
            "¿Cuál es el café más peligroso del mundo? El ex-preso.",
            "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
            "¿Qué hace un perro con un taladro? Ta-drando.",
            "¿Cómo se dice 'perdí el autobús' en alemán? Suban-estrujen-bajen.",
            "¿Qué le dice una impresora a otra? ¿Esa copia es tuya o es impresión mía?",
            "¿Por qué el libro de matemáticas se suicidó? Porque tenía muchos problemas."
        ]

    def tirar_gacha(self):
        """Lógica para cobrar fichas y devolver un chiste aleatorio"""
        if self.usuarios[self.uid]["fichas"] < self.costo:
            return {"error": "Fichas insuficientes", "costo": self.costo}

        self.usuarios[self.uid]["fichas"] -= self.costo
        
        chiste = random.choice(self.lista_chistes)

        self.guardar_datos(self.usuarios)

        return {
            "resultado": "éxito",
            "chiste": chiste,
            "costo": self.costo,
            "fichas_restantes": self.usuarios[self.uid]["fichas"]
        }