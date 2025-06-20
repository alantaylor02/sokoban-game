# sokoban-game

Trabajo práctico realizado durante la cursada de Algoritmos y Programación 1 de Ingeniería en Informática, Universidad de Buenos Aires.

---

## Descripción general

Este proyecto es una implementación del clásico juego Sokoban, desarrollada como trabajo práctico. El objetivo del juego es que el jugador mueva cajas hasta ubicarlas en los objetivos marcados en el mapa, respetando las reglas de movimiento del Sokoban clásico.

## Funcionalidades implementadas

- **Carga dinámica de niveles:** Los niveles se cargan desde un archivo de texto, permitiendo jugar múltiples escenarios y avanzar cuando se completa uno.
- **Controles personalizables:** Las teclas para mover al jugador y ejecutar acciones están definidas en un archivo y pueden ser modificadas.
- **Mecánica de movimiento:** El jugador puede moverse en las cuatro direcciones y empujar cajas siguiendo las reglas tradicionales del Sokoban.
- **Sistema de deshacer y rehacer:** Se pueden deshacer y rehacer movimientos utilizando una pila para registrar jugadas y otra para jugadas deshechas.
- **Reinicio de nivel:** Es posible reiniciar el nivel en cualquier momento para empezar desde el estado inicial.
- **Pistas automáticas:** El sistema puede calcular y mostrar una secuencia de movimientos que resuelve el nivel actual, utilizando un algoritmo de backtracking.
- **Gestión de múltiples niveles:** Al completar un nivel, el juego avanza automáticamente al siguiente, hasta finalizar todos los disponibles.
- **Mensajes interactivos:** El juego muestra mensajes para informar si el nivel ya no se puede ganar o si hay pistas disponibles.
- **Interfaz gráfica sencilla:** Se utiliza la librería `gamelib` para renderizar la grilla y los elementos del juego de forma visual.

## Tecnologías y lenguajes utilizados

- **Lenguaje principal:** Python
- **Librerías utilizadas:**
  - `gamelib` para la interfaz gráfica del juego.
- **Estructuras de datos personalizadas:**
  - Implementación propia de pilas y colas para gestionar jugadas y pistas.
- **Archivos auxiliares:**
  - `niveles.txt` para los mapas de juego.
  - `teclas.txt` para la configuración de los controles.

## Estructura del código

- `sokoban/main.py`: Lógica principal del juego, bucle de juego, gestión de eventos y renderizado.
- `sokoban/soko.py`: Funciones relacionadas con la lógica del Sokoban, como movimientos, estados y verificación de victoria.
- `sokoban/pila.py` y `sokoban/cola.py`: Implementaciones de pila y cola utilizadas para deshacer/rehacer movimientos y pistas.
- `sokoban/niveles.txt`: Colección de mapas de niveles.
- `sokoban/teclas.txt`: Configuración de teclas para el control del juego.

---

## Cómo ejecutar

1. Instalar Python 3.
2. Instalar la librería `gamelib` si no está disponible.
3. Ejecutar el archivo principal (`main.py`).

```bash
python3 sokoban/main.py
```