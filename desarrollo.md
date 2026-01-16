#### CacinHub

CacinHub es un proyecto de casino en consola desarrollado en Python, creado como parte de un proyecto académico de nivel A2.
El objetivo es simular un casino interactivo donde el usuario puede apostar, jugar y gestionar su saldo mediante diferentes juegos basados en azar.

El proyecto está diseñado para ser modular, claro, y con una buena gestión del flujo del juego y de los errores.

### Características principales

Interfaz en consola limpia e interactiva

Sistema de usuario con saldo e historial

Juegos basados en números aleatorios

Validación de apuestas y control de errores

Flujo de juego continuo hasta que el usuario decida salir

### Herramientas y librerías utilizadas

Este proyecto utiliza únicamente librerías integradas de Python, por lo que no es necesario instalar dependencias externas.

## Librerías principales

# random
# time
# os

## Estructura de datos

Datos del jugador
Componente 	    Descripción
Saldo	        Cantidad de dinero actual del jugador
Historial	    Lista que guarda si ganó o perdió en rondas anteriores
Apuesta mínima	Valor constante para evitar apuestas inválidas

Ejemplo:

jugador = {
    "nombre": "",
    "saldo": 100,
    "historial": []
}

### Lógica del flujo de juego

CacinHub funciona mediante un bucle principal (while), lo que permite que el casino siga activo hasta que el jugador decida salir o se quede sin saldo.

## Flujo del programa

# Inicio: 
Carga de datos desde casino_db.json o creación de nuevo perfil.

# Lógica de Juego: 
Validación de fondos -> Ejecución de azar -> Cálculo de puntos.

# Actualización: 
El estado del jugador se guarda en el archivo JSON tras cada acción importante.

# Bienvenida
Se muestra el logo y el mensaje inicial de CacinHub.

# Registro / Inicio
El jugador introduce su nombre y su saldo inicial.

# Menú principal
El usuario puede:

Elegir un juego

Ver su saldo

Salir del casino

## Validación de apuestas
Se comprueba que el jugador:

Tenga saldo suficiente
No apueste valores negativos o cero
Resultado del juego
Se ejecuta la lógica aleatoria y se actualiza el saldo y el historial.

### Objetivos del proyecto

Estafar gente

Simular un sistema real de apuestas

Garantizar que las apuestas y el saldo nunca generen estados inconsistentes.
