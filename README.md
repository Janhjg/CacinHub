## CacinHub API 
API de casino desarrollada en Python
## Descripción
CacinHub es una API que simula un sistema de casino donde los usuarios pueden:

* Registrarse y autenticarse
* Gestionar su saldo mediante transacciones
* Apostar en diferentes juegos de azar
* Consultar historial de partidas
* Persistir datos entre sesiones

El proyecto sigue un enfoque de desarrollo incremental, implementando funcionalidades de forma progresiva con testing continuo.

## Enfoque de Desarrollo
1. Definición y Diseño
Problema a resolver:

Crear una API de casino funcional que permita a los usuarios gestionar su perfil, realizar apuestas y jugar diferentes juegos de azar de manera segura.

Funcionalidades principales:

* Sistema de registro y autenticación de usuarios
* Gestión de saldo y transacciones
* Points para múltiples juegos de azar
* Persistencia de datos (JSON/Base de datos)
* Historial de partidas por usuario

# 2. Diseño Funcional
## Gestión de Usuarios
Crear usuario
* Qué hace: Registra un nuevo jugador en el sistema
* Recibe: Nombre del usuario y saldo inicial
* Devuelve: Datos del usuario creado con su ID
#### Puede fallar si: El nombre ya existe o el saldo es menor a 10

## Consultar usuario

* Qué hace: Obtiene la información de un jugador
* Recibe: ID del usuario
* Devuelve: Nombre, saldo actual y fecha de registro
#### Puede fallar si: El usuario no existe

## Añadir saldo

* Qué hace: Incrementa el saldo de un usuario
* Recibe: ID del usuario y cantidad a depositar
* Devuelve: Nuevo saldo actualizado
#### Puede fallar si: La cantidad es 0 o negativa

## Gestión de Juegos
Listar juegos
* Qué hace: Muestra todos los juegos disponibles
* Recibe: Nada
* Devuelve: Lista con nombre, reglas y apuesta mínima de cada juego
#### Puede fallar si: (no aplica)

## Realizar apuesta

* Qué hace: Ejecuta una partida en el juego seleccionado
* Recibe: ID del usuario, cantidad apostada y opciones del juego
* Devuelve: Resultado (ganó/perdió), ganancia y saldo actualizado
* Puede fallar si: Saldo insuficiente, apuesta inválida o juego no existe

## Historial
Ver historial de partidas

* Qué hace: Lista todas las partidas jugadas por un usuario
* Recibe: ID del usuario (opcionalmente un límite de resultados)
* Devuelve: Lista de partidas con fecha, juego, apuesta y resultado
#### Puede fallar si: El usuario no existe

# 3. Testing desde el Inicio
Los tests garantizan el correcto funcionamiento de cada endpoint desde el inicio del desarrollo.
## Cobertura de tests:

* Tests de endpoints (status codes, respuestas JSON)
* Validación de datos de entrada
* Lógica de cada juego (probabilidades, pagos)
* Integridad de datos (saldo nunca negativo)
* Persistencia correcta en base de datos

## Ejecutar tests:
* Pytest

# 4. Implementación Progresiva
El proyecto evoluciona desde una estructura simple.
### Fase 1 - API básica:

* Endpoints fundamentales (crear usuario, obtener saldo)
* Validación básica de datos
* Almacenamiento en JSON
* Un juego (o dos) simple implementado

### Fase 2 - Ampliación y validación:

* Más juegos disponibles
* Validaciones completas en cada endpoint

## Librerías y herramientas estándar:

* random - Generación de números aleatorios para juegos
* json - Persistencia de datos (fase inicial)
* datetime - Timestamps de partidas (opcional)

# Juegos Disponibles
### 1. Ruleta
#### Opciones:
* rojo o negro: pago x2
* numero (0-36): pago x36

### 2. Dados
#### Opciones:

Suma específica (2-12): Con una probabilidad variable.

### 3. Tragamonedas
#### Mecánica:

* Tres símbolos aleatorios
* Combinaciones ganadoras con pagos de x2 a x100

# Objetivos
#### Este proyecto tiene como finalidad:
* Diseñar e implementar una API funcional
* Trabajar con persistencia de datos JSON - Base de datos
* Desarrollar lógica de negocio (juegos de azar)
