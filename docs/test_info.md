# Test principales

## Gestion de usuarios 

### Test Creacion de usuario 

1. Verificacion de creacion exitosa 

Qué hace: Comprueba que un usuario se crea correctamente
Recibe: Nombre único y saldo válido (≥10)
Devuelve: Usuario con ID único generado y datos guardados en BD
Debe pasar si: Los datos son válidos y el nombre no existe

2. Rechazo de nombres duplicados

- Qué hace: Comprueba que el sistema detecta nombres repetidos
- Recibe: Nombre que ya existe en el sistema
- Devuelve: Error indicando que el nombre ya está registrado
- Debe pasar si: El sistema rechaza el duplicado correctamente

3. Validacion de saldo inicial

- Qué hace: Comprueba que el sistema valida el saldo inicial
- Recibe: Saldo menor a 10
- Devuelve: Error indicando saldo insuficiente
- Debe pasar si: El sistema rechaza saldos menores a 100

### Test Consultar usuario 

test_name: test_consultar_usuario

1. Usuario existente 

test_name: test_consultar_usuario_existente

- Qué hace: Comprueba que se obtienen los datos de un usuario válido
- Recibe: ID de un usuario existente
- Devuelve: Nombre, saldo y fecha de registro del usuario
- Debe pasar si: El ID existe y devuelve todos los campos correctos

2. Usuario inexistente

test_name: test_consultar_usuario_inexistente

- Qué hace: Comprueba que el sistema detecta IDs inválidos
- Recibe: ID que no existe en el sistema
- Devuelve: Error indicando que el usuario no fue encontrado
- Debe pasar si: El sistema rechaza correctamente el ID inexistente

### Test añadir saldo 

1. Incremento de saldo

- Qué hace: Comprueba que el saldo se incrementa correctamente
- Recibe: ID válido y cantidad positiva
- Devuelve: Saldo actualizado (saldo anterior + cantidad depositada)
- Debe pasar si: El nuevo saldo refleja la suma correcta

2. Rechazo cantidad 0

- Qué hace: Comprueba que el sistema rechaza depósitos de 0
- Recibe: Cantidad igual a 0
- Devuelve: Error indicando que la cantidad debe ser mayor a 0
- Debe pasar si: El sistema rechaza correctamente el valor 0

3. Rechazo cantidad negativa

- Qué hace: Comprueba que el sistema rechaza cantidades negativas
- Recibe: Cantidad menor a 0
- Devuelve: Error indicando que la cantidad debe ser positiva
- Debe pasar si: El sistema rechaza correctamente valores negativos

## Test Gestion de jeugos 

### Test listar juegos 

1. checklist de juegos 

- Qué hace: Comprueba que se obtienen todos los juegos registrados
- Recibe: Nada
- Devuelve: Array con todos los juegos del sistema
- Debe pasar si: La cantidad de juegos coincide con los registrados

2. Esctructura juego 

- Qué hace: Comprueba que cada juego tiene todos sus campos
- Recibe: Nada
- Devuelve: Cada juego con nombre, reglas y apuesta mínima
- Debe pasar si: Todos los juegos contienen los campos requeridos

### Test Realizar apuesta 

1. Apuesta valida 

- Qué hace: Comprueba que se ejecuta una partida correctamente
- Recibe: ID válido, apuesta válida y juego existente
- Devuelve: Resultado (ganó/perdió), ganancia y saldo actualizado
- Debe pasar si: El juego se ejecuta y devuelve todos los campos

2. Actualizacion de saldo

- Qué hace: Comprueba que el saldo se actualiza según el resultado
- Recibe: Apuesta válida y juego que produce resultado
- Devuelve: Saldo incrementado (si gana) o decrementado (si pierde)
- Debe pasar si: El saldo refleja correctamente ganancia o pérdida

3. Rechazo de saldo insuficiente

- Qué hace: Comprueba que detecta cuando no hay suficiente saldo
- Recibe: Apuesta mayor al saldo disponible del usuario
- Devuelve: Error indicando saldo insuficiente
- Debe pasar si: El sistema rechaza la apuesta correctamente

4. Validacion apuesta minima

- Qué hace: Comprueba que se respeta la apuesta mínima del juego
- Recibe: Apuesta menor al mínimo requerido del juego
- Devuelve: Error indicando que la apuesta es menor al mínimo
- Debe pasar si: El sistema rechaza apuestas bajo el mínimo

5. Rechazo juego inexistente

- Qué hace: Comprueba que detecta juegos que no existen
- Recibe: Nombre de juego no registrado en el sistema
- Devuelve: Error indicando que el juego no existe
- Debe pasar si: El sistema rechaza correctamente el juego inválido

### Test Historial

1. Historial completo

- Qué hace: Comprueba que se obtienen todas las partidas del usuario
- Recibe: ID de usuario con partidas registradas
- Devuelve: Array con todas las partidas (fecha, juego, apuesta, resultado)
- Debe pasar si: Todas las partidas están presentes con sus datos completos

2. Limite de resultados

- Qué hace: Comprueba que se respeta el límite especificado
- Recibe: ID de usuario y número límite de resultados
- Devuelve: Array con cantidad de partidas igual o menor al límite
- Debe pasar si: La cantidad de partidas no excede el límite indicado

3. Error usuario inexistente

- Qué hace: Comprueba que detecta IDs inválidos en el historial
- Recibe: ID de usuario que no existe
- Devuelve: Error indicando que el usuario no fue encontrado
- Debe pasar si: El sistema rechaza correctamente el ID inexistente

4. Usuario sin partidas

- Qué hace: Comprueba el comportamiento con usuarios nuevos
- Recibe: ID de usuario que no ha jugado ninguna partida
- Devuelve: Array vacío []
- Debe pasar si: Devuelve un array vacío sin errores