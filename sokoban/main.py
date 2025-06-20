import soko
import gamelib
from cola import Cola
from pila import Pila

ANCHO_IMAGEN, ALTO_IMAGEN = 64, 64
PISO = " "
PARED = "#"
CAJA = "$"
JUGADOR = "@"
OBJETIVO = "."
OBJETIVO_Y_CAJA = "*"
OBJETIVO_Y_JUGADOR = "+"

def hacer_grilla_perfecta(grilla):
    """Recibe una grilla y la convierte en una
    de dimensiones perfectas
    """
    fila_mas_larga = max(grilla, key=len)
    long_fila_mas_larga = len(fila_mas_larga)

    for fila in grilla:
        for i in range(long_fila_mas_larga - len(fila)):
            fila.append(" ")
    
    return grilla

def obtener_teclas(archivo_teclas):
    """Recibe el archivo de las teclas, lo lee y devuelve
    un diccionario con las mismas y sus acciones
    """
    dic_teclas = {}

    with open(archivo_teclas) as teclas:

        for linea in teclas:

            linea = linea.rstrip()

            if linea == "":
                continue

            tecla, accion = linea.split(" = ")
            
            dic_teclas[tecla] = accion
    
    return dic_teclas

def obtener_niveles(archivo_niveles):
    """Recibe un archivo de niveles, lo lee y devuelve
    un diccionario con el número de nivel como clave
    y la descripción del mismo
    """
    dic_niveles = {}
    
    with open(archivo_niveles) as niveles:

        desc = []
        nivel = 1

        for linea in niveles:

            linea = linea.rstrip()

            if linea != "" and linea[0] != "L" and linea[0] != "'":

                desc.append(linea)
                continue
            
            if linea == "":
                
                dic_niveles[nivel] = desc
                nivel += 1
                desc = []

    return dic_niveles

def obtener_direccion(accion):
    """Recibe la acción asociada a una tecla
    (si ésta es de movimiento), y devuelve la
    dirección en la que se efectúa el mismo
    """
    acciones = {"NORTE": (0, -1), "SUR": (0, 1), "OESTE": (-1, 0), "ESTE": (1, 0)}

    return acciones[accion]

def pixel_donde_dibujar(f, c):
    """Recibe la fila y columna de la celda en 
    la que estoy, y devuelve el pixel donde se 
    va a dibujar el símbolo.
    """
    x = c * ANCHO_IMAGEN
    y = f * ALTO_IMAGEN

    return x, y

def deshacer(pila_jugadas, pila_deshechas):
    
    jugada_a_deshacer = pila_jugadas.desapilar()

    if pila_jugadas.esta_vacia():

        pila_jugadas.apilar(jugada_a_deshacer)

        return pila_jugadas.ver_tope() 

    pila_deshechas.apilar(jugada_a_deshacer)
    jugada_anterior = pila_jugadas.ver_tope()

    return jugada_anterior

def rehacer(pila_jugadas, pila_deshechas):

    if not pila_deshechas.esta_vacia():

        jugada_a_rehacer = pila_deshechas.desapilar()
        pila_jugadas.apilar(jugada_a_rehacer)

        return jugada_a_rehacer
    
    return pila_jugadas.ver_tope()

def crear_pilas_vacias_y_agregar_jugada(grilla):

    pila_jugadas = Pila()
    pila_jugadas.apilar(grilla)
    pila_deshechas = Pila()

    return pila_jugadas, pila_deshechas

def pasar_grilla_a_tupla(grilla):

    lista_res = []

    for fila in grilla:
        fila = tuple(fila)
        lista_res.append(fila)
        
    return tuple(lista_res)

def buscar_solucion(grilla_inicial):

    visitados = set()
    direcciones = ((1, 0), (-1, 0), (0, 1), (0, -1))

    return backtrack(grilla_inicial, visitados, direcciones)

def backtrack(grilla, visitados, direcciones):

    visitados.add(pasar_grilla_a_tupla(grilla))

    if soko.juego_ganado(grilla):
        # ¡Encontramos la solución!
        return True, []
    
    for direccion in direcciones:

        nuevo_estado = soko.mover(grilla, direccion)

        if pasar_grilla_a_tupla(nuevo_estado) in visitados:
            continue
        
        solucion_encontrada, direcciones_a_mover = backtrack(nuevo_estado, visitados, direcciones)

        if solucion_encontrada:
            return True, [direccion] + direcciones_a_mover
    
    return False, None

def guardar_pistas(grilla_actual, cola_pistas):
    """Recibe la grilla actual y la cola de pistas. Busca la solucion de la grilla actual
    y devuelve la cola de pistas con todos los movimientos necesarios para completar el nivel.
    Si el nivel ya no puede ser completado, devuelve None.
    """
    solucion_encontrada, direcciones_a_mover = buscar_solucion(grilla_actual)
    
    if solucion_encontrada:

        for direccion in direcciones_a_mover:

            cola_pistas.encolar(direccion)
        
        return cola_pistas
    
    return None
    
def mostrar_pistas(grilla_actual, cola_pistas):
    """Recibe la grilla actual y la cola de pistas.
    Devuelve la grilla de la cola de pistas que esta al frente
    (si hay disponibles) y sino muestra la grilla actual.
    """
    if not cola_pistas.esta_vacia():

        direccion_pista = cola_pistas.desencolar()
        grilla_pista = soko.mover(grilla_actual, direccion_pista)

        return grilla_pista
    
    return grilla_actual

def realizar_accion_segun_tecla(grilla, archivos_cargados, estado_actual, pilas, cola_pistas):
    """Recibe la grilla, una tupla con los archivos de niveles y teclas, 
    otra con la tecla presionada y el nivel actual, una tupla con las pilas de jugadas 
    y jugadas deshechas, y tambien la cola donde se almacenan las pistas.

    Devuelve la grilla correspondiente dependiendo de la tecla pulsada, y tambien modifica las
    pilas recibididas y la cola de pistas según la tecla presionada.
    """
    teclas, niveles = archivos_cargados
    tecla_pulsada, nivel_actual = estado_actual
    pila_jugadas, pila_deshechas = pilas

    if teclas[tecla_pulsada] == "REINICIAR":
        grilla = hacer_grilla_perfecta(soko.crear_grilla(niveles[nivel_actual]))
        pila_jugadas, pila_deshechas = crear_pilas_vacias_y_agregar_jugada(grilla)
        cola_pistas = Cola()
    
    elif teclas[tecla_pulsada] == "SALIR":
        grilla = None
    
    elif teclas[tecla_pulsada] == "DESHACER":
        grilla = deshacer(pila_jugadas, pila_deshechas)
        cola_pistas = Cola()

    elif teclas[tecla_pulsada] == "REHACER":
        grilla = rehacer(pila_jugadas, pila_deshechas)
    
    elif teclas[tecla_pulsada] == "PISTAS":

        if cola_pistas is not None:

            if cola_pistas.esta_vacia():
                cola_pistas = guardar_pistas(grilla, cola_pistas)

            else:    
                grilla = mostrar_pistas(grilla, cola_pistas)

                pila_jugadas.apilar(grilla)
            
    else:
        grilla = soko.mover(grilla, obtener_direccion(teclas[tecla_pulsada]))
        pila_deshechas = Pila()
        cola_pistas = Cola()

        if grilla != pila_jugadas.ver_tope():

            pila_jugadas.apilar(grilla)

    return grilla, pila_jugadas, pila_deshechas, cola_pistas

def grilla_mostrar(grilla):
    """Recibe la grilla, interpreta cada símbolo buscándolo en
    el diccionario y dibuja por la pantalla de gamelib la misma
    """
    imagenes = {PISO: 'img/ground.gif', PARED: 'img/wall.gif', CAJA: 'img/box.gif', JUGADOR: 'img/player.gif',
    OBJETIVO: 'img/goal.gif', OBJETIVO_Y_CAJA: ('img/box.gif', 'img/goal.gif'), OBJETIVO_Y_JUGADOR: ('img/goal.gif', 'img/player.gif')}

    for f in range(len(grilla)):
        for c in range(len(grilla[0])):

            x, y = pixel_donde_dibujar(f, c)

            gamelib.draw_image(imagenes[PISO], x, y)
            
            if grilla[f][c] in imagenes:

                if len(imagenes[grilla[f][c]]) == 2:

                    gamelib.draw_image(imagenes[grilla[f][c]][0], x, y)
                    gamelib.draw_image(imagenes[grilla[f][c]][1], x, y)
                    continue

                gamelib.draw_image(imagenes[grilla[f][c]], x, y)

def main():

    try: 
        archivos_cargados = (obtener_teclas("teclas.txt"), obtener_niveles("niveles.txt"))
        teclas, niveles = archivos_cargados
        
        nivel = 1
        grilla = hacer_grilla_perfecta(soko.crear_grilla(niveles[nivel]))

        pila_jugadas, pila_deshechas = crear_pilas_vacias_y_agregar_jugada(grilla)
        pilas = pila_jugadas, pila_deshechas
        cola_pistas = Cola()

        ancho_ventana, alto_ventana = ANCHO_IMAGEN * len(grilla[0]), ALTO_IMAGEN * len(grilla)
        gamelib.resize(ancho_ventana, alto_ventana)

        while gamelib.is_alive():

            gamelib.draw_begin()
            grilla_mostrar(grilla)

            if cola_pistas is None: # La cola de pistas no existe porque el nivel ya no se puede ganar, entonces mostrar el siguiente mensaje
                gamelib.draw_text("Ya no se puede ganar, es necesario reiniciar", 5, 5, anchor='nw')

            elif not cola_pistas.esta_vacia(): # Si la cola de pistas existe y no está vacía, mostrar el siguiente mensaje
                gamelib.draw_text("Pistas disponibles", 5, 5, anchor='nw')

            gamelib.draw_end()

            ev = gamelib.wait(gamelib.EventType.KeyPress)
            if not ev:
                break

            tecla = ev.key
        
            if tecla in teclas:

                estado_actual = tecla, nivel
                
                grilla, pila_jugadas, pila_deshechas, cola_pistas = realizar_accion_segun_tecla(grilla, archivos_cargados, estado_actual, pilas, cola_pistas)
                pilas = pila_jugadas, pila_deshechas

                if grilla == None:
                    break

            if soko.juego_ganado(grilla):

                nivel += 1

                if nivel not in niveles:
                    break

                grilla = hacer_grilla_perfecta(soko.crear_grilla(niveles[nivel]))
                
                pila_jugadas, pila_deshechas = crear_pilas_vacias_y_agregar_jugada(grilla)
                pilas = pila_jugadas, pila_deshechas
                cola_pistas = Cola()

                ancho_ventana, alto_ventana = ANCHO_IMAGEN * len(grilla[0]), ALTO_IMAGEN * len(grilla)
                gamelib.resize(ancho_ventana, alto_ventana)

    except FileNotFoundError as e:
        print("No se ha encontrado el archivo:", e)

gamelib.init(main)