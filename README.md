# CacinHub API 
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
* Endpoints para múltiples juegos de azar
* Persistencia de datos (JSON/Base de datos)
* Historial de partidas por usuario

# 2. Diseño Funcional
## Gestión de Usuarios

#### Crear usuario

Qué hace: Registra un nuevo jugador en el sistema
Recibe: Nombre del usuario y contraseña
Devuelve: Datos del usuario creado con su ID (único)
Puede fallar si: El nombre ya existe o el saldo es menor a 10

###### ( input : dime tu nombre y contrasena
print : nombre - Takaka contrasena : 123 ID : ????
(cantidad inicial minimo 100))

### Tests
#### * Test 1: Verificar creación exitosa con datos válidos

Qué hace: Comprueba que un usuario se crea correctamente
Recibe: Nombre único y saldo válido (≥10)
Devuelve: Usuario con ID único generado y datos guardados en BD
Debe pasar si: Los datos son válidos y el nombre no existe

#### * Test 2: Verificar rechazo de nombres duplicados

Qué hace: Comprueba que el sistema detecta nombres repetidos
Recibe: Nombre que ya existe en el sistema
Devuelve: Error indicando que el nombre ya está registrado
Debe pasar si: El sistema rechaza el duplicado correctamente

#### * Test 3: Verificar validación de saldo mínimo

Qué hace: Comprueba que el sistema valida el saldo inicial
Recibe: Saldo menor a 10
Devuelve: Error indicando saldo insuficiente
Debe pasar si: El sistema rechaza saldos menores a 10


### Consultar usuario

Qué hace: Obtiene la información de un jugador.
Recibe: ID del usuario
Devuelve: Nombre, saldo actual y fecha de registro
Puede fallar si: El usuario no existe

### Tests
#### * Test 1: Verificar consulta exitosa de usuario existente

Qué hace: Comprueba que se obtienen los datos de un usuario válido
Recibe: ID de un usuario existente
Devuelve: Nombre, saldo y fecha de registro del usuario
Debe pasar si: El ID existe y devuelve todos los campos correctos

* Test 2: Verificar error con ID inexistente

Qué hace: Comprueba que el sistema detecta IDs inválidos
Recibe: ID que no existe en el sistema
Devuelve: Error indicando que el usuario no fue encontrado
Debe pasar si: El sistema rechaza correctamente el ID inexistente


### Añadir saldo

Qué hace: Incrementa el saldo de un usuario
Recibe: ID del usuario y cantidad a depositar
Devuelve: Nuevo saldo actualizado
Puede fallar si: La cantidad es 0 o negativa

### Tests
#### * Test 1: Verificar incremento correcto con cantidad válida

Qué hace: Comprueba que el saldo se incrementa correctamente
Recibe: ID válido y cantidad positiva
Devuelve: Saldo actualizado (saldo anterior + cantidad depositada)
Debe pasar si: El nuevo saldo refleja la suma correcta

#### * Test 2: Verificar rechazo de cantidad cero

Qué hace: Comprueba que el sistema rechaza depósitos de 0
Recibe: Cantidad igual a 0
Devuelve: Error indicando que la cantidad debe ser mayor a 0
Debe pasar si: El sistema rechaza correctamente el valor 0

#### * Test 3: Verificar rechazo de cantidades negativas

Qué hace: Comprueba que el sistema rechaza cantidades negativas
Recibe: Cantidad menor a 0
Devuelve: Error indicando que la cantidad debe ser positiva
Debe pasar si: El sistema rechaza correctamente valores negativos


### * Gestión de Juegos
Listar juegos

Qué hace: Muestra todos los juegos disponibles
Recibe: Nada
Devuelve: Lista con nombre, reglas y apuesta mínima de cada juego
Puede fallar si: (no aplica)

### TestsE
#### * Test 1: Verificar que devuelve todos los juegos

Qué hace: Comprueba que se obtienen todos los juegos registrados
Recibe: Nada
Devuelve: Array con todos los juegos del sistema
Debe pasar si: La cantidad de juegos coincide con los registrados

#### * Test 2: Verificar estructura completa de cada juego

Qué hace: Comprueba que cada juego tiene todos sus campos
Recibe: Nada
Devuelve: Cada juego con nombre, reglas y apuesta mínima
Debe pasar si: Todos los juegos contienen los campos requeridos


### Realizar apuesta

Qué hace: Ejecuta una partida en el juego seleccionado
Recibe: ID del usuario, cantidad apostada y opciones del juego
*** "resta de saldo" y actualiza **** 
Devuelve: Resultado (ganó/perdió), ganancia y saldo actualizado
Puede fallar si: Saldo insuficiente, apuesta inválida o juego no existe

### Tests
#### * Test 1: Verificar procesamiento de apuesta válida

Qué hace: Comprueba que se ejecuta una partida correctamente
Recibe: ID válido, apuesta válida y juego existente
Devuelve: Resultado (ganó/perdió), ganancia y saldo actualizado
Debe pasar si: El juego se ejecuta y devuelve todos los campos

#### * Test 2: Verificar actualización correcta de saldo

Qué hace: Comprueba que el saldo se actualiza según el resultado
Recibe: Apuesta válida y juego que produce resultado
Devuelve: Saldo incrementado (si gana) o decrementado (si pierde)
Debe pasar si: El saldo refleja correctamente ganancia o pérdida

#### * Test 3: Verificar rechazo por saldo insuficiente

Qué hace: Comprueba que detecta cuando no hay suficiente saldo
Recibe: Apuesta mayor al saldo disponible del usuario
Devuelve: Error indicando saldo insuficiente
Debe pasar si: El sistema rechaza la apuesta correctamente

#### * Test 4: Verificar validación de apuesta mínima

Qué hace: Comprueba que se respeta la apuesta mínima del juego
Recibe: Apuesta menor al mínimo requerido del juego
Devuelve: Error indicando que la apuesta es menor al mínimo
Debe pasar si: El sistema rechaza apuestas bajo el mínimo

#### * Test 5: Verificar rechazo de juego inexistente

Qué hace: Comprueba que detecta juegos que no existen
Recibe: Nombre de juego no registrado en el sistema
Devuelve: Error indicando que el juego no existe
Debe pasar si: El sistema rechaza correctamente el juego inválido


### Historial
Ver historial de partidas (guarde la cantidad de partidas total y de cada juego)
"crear un usuario demo"

Qué hace: Lista todas las partidas jugadas por un usuario
Recibe: ID del usuario (opcionalmente un límite de resultados)
Devuelve: Lista de partidas con fecha, juego, apuesta y resultado
Puede fallar si: El usuario no existe

#### Paquito
juego: dados
apuesta: 10
jugador:6
banca:2
partida : win/lose
ganacia: 20
saldo: 30

### Tests
#### * Test 1: Verificar obtención de historial completo

Qué hace: Comprueba que se obtienen todas las partidas del usuario
Recibe: ID de usuario con partidas registradas
Devuelve: Array con todas las partidas (fecha, juego, apuesta, resultado)
Debe pasar si: Todas las partidas están presentes con sus datos completos

#### * Test 2: Verificar funcionamiento del límite de resultados

Qué hace: Comprueba que se respeta el límite especificado
Recibe: ID de usuario y número límite de resultados
Devuelve: Array con cantidad de partidas igual o menor al límite
Debe pasar si: La cantidad de partidas no excede el límite indicado

#### * Test 3: Verificar error con usuario inexistente

Qué hace: Comprueba que detecta IDs inválidos en el historial
Recibe: ID de usuario que no existe
Devuelve: Error indicando que el usuario no fue encontrado
Debe pasar si: El sistema rechaza correctamente el ID inexistente

#### * Test 4: Verificar respuesta con usuario sin partidas

Qué hace: Comprueba el comportamiento con usuarios nuevos
Recibe: ID de usuario que no ha jugado ninguna partida
Devuelve: Array vacío []
Debe pasar si: Devuelve un array vacío sin errores

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

# Juegos Disponibles (opciones)
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

