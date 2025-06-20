PARED = "#"
CAJA = "$"
JUGADOR = "@"
OBJETIVO = "."
OBJETIVO_Y_CAJA = "*"
OBJETIVO_Y_JUGADOR = "+" 
VACIO = " "

def crear_grilla(desc):
    
    grilla = []

    for fila in desc:
        grilla.append(list(fila))
    
    return grilla

def dimensiones(grilla):

    columnas = 0
    filas = 0

    for fila in grilla:
        filas += 1
    
    for columna in grilla[0]:
        columnas += 1
   
    return columnas, filas

def hay_vacio(grilla, c, f):
    return grilla[f][c] == VACIO
    
def hay_pared(grilla, c, f):
    return grilla[f][c] == PARED
    
def hay_objetivo(grilla, c, f):
    return grilla[f][c] == OBJETIVO or grilla[f][c] == OBJETIVO_Y_CAJA or grilla[f][c] == OBJETIVO_Y_JUGADOR

def hay_caja(grilla, c, f):
    return grilla[f][c] == CAJA or grilla[f][c] == OBJETIVO_Y_CAJA
    
def hay_jugador(grilla, c, f):
    return grilla[f][c] == JUGADOR or grilla[f][c] == OBJETIVO_Y_JUGADOR
    
def juego_ganado(grilla):

    cajas = 0
    cajas_y_objetivos = 0

    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            
            if grilla[f][c] == CAJA:
                cajas += 1
            
            elif grilla[f][c] == OBJETIVO_Y_CAJA:
                cajas_y_objetivos += 1
                cajas += 1

    return cajas == cajas_y_objetivos    
            
def copiar_grilla(grilla):
    """
    Recibe una lista que representa una grilla y devuelve
    el contenido de la misma en otra lista distinta.
    """
    copia_grilla = []

    for elemento in grilla:
        copia_grilla.append(elemento[:])
    
    return copia_grilla

def cambiar_contenido_celdas(grilla, direccion, valores_a_cambiar, pos_jugador):
    """
    Recibe una lista que representa una grilla, la dirección
    del movimiento en forma de una tupla, los valores a cambiar de las
    celdas en las que se va a mover el jugador en forma de una tupla y la posición
    donde se encuentra el jugador tambien en forma de tupla.
    Devuelve una nueva grilla con los valores cambiados en las respectivas
    celdas, o devuelve la grilla original si no hay valores a cambiar.

    - Si "valores_a_cambiar" es una tupla vacia, no hay nada para cambiar entonces
    devuelve la grilla original.

    - Si en "valores_a_cambiar" hay 2 elementos, se modificará la celda donde
    estaba el jugador y la celda vecina en la dirección del movimiento, con los
    respectivos elementos de la tupla.

    - Si en "valores_a_cambiar" hay 3 elementos, se modificará lo mismo que en
    el caso anterior, pero a su vez se modificará la celda que le sigue a la vecina,
    con los respectivos elementos de la tupla.
    """
    mov_c, mov_f = direccion
    grilla_res = []
    c, f = pos_jugador

    if not valores_a_cambiar:

        return grilla
    
    if len (valores_a_cambiar) >= 2:

        grilla_res = copiar_grilla(grilla)
        grilla_res[f][c] = valores_a_cambiar[0]
        grilla_res[f + mov_f][c + mov_c] = valores_a_cambiar[1]

        if len(valores_a_cambiar) == 3:
                
            grilla_res[f + 2 * mov_f][c + 2 * mov_c] = valores_a_cambiar[2]
    
    return grilla_res

def obtener_caracteres_a_cambiar(grilla, direccion, pos_jugador, caracter_celda_jugador):
    """
    Recibe la grilla, la direccion del movimiento en forma de tupla,
    la posición del jugador en forma de tupla y el carácter que irá
    en la posición donde estaba el jugador.

    Devuelve una tupla con los caracteres que se van a cambiar en la
    dirección del movimiento del jugador.
    """
    c, f = pos_jugador
    mov_c, mov_f = direccion
    caracteres_a_cambiar = ()
    
    if caracter_celda_jugador == VACIO or caracter_celda_jugador == OBJETIVO:

        if hay_vacio(grilla, c + mov_c, f + mov_f):

            caracteres_a_cambiar = (caracter_celda_jugador, JUGADOR)
                
        if grilla[f + mov_f][c + mov_c] == OBJETIVO:

            caracteres_a_cambiar = (caracter_celda_jugador, OBJETIVO_Y_JUGADOR)
                
        if grilla[f + mov_f][c + mov_c] == OBJETIVO_Y_CAJA:
                    
            if hay_vacio(grilla, c + 2 * mov_c, f + 2 * mov_f):

                caracteres_a_cambiar = (caracter_celda_jugador, OBJETIVO_Y_JUGADOR, CAJA)
                    
            if grilla[f + 2 * mov_f][c + 2 * mov_c] == OBJETIVO:

                caracteres_a_cambiar = (caracter_celda_jugador, OBJETIVO_Y_JUGADOR, OBJETIVO_Y_CAJA)

        if grilla[f + mov_f][c + mov_c] == CAJA:

            if hay_vacio(grilla, c + 2 * mov_c, f + 2 * mov_f):

                caracteres_a_cambiar = (caracter_celda_jugador, JUGADOR, CAJA)
                                            
            if grilla[f + 2 * mov_f][c + 2 * mov_c] == OBJETIVO:

                caracteres_a_cambiar = (caracter_celda_jugador, JUGADOR, OBJETIVO_Y_CAJA)

    return caracteres_a_cambiar

def mover(grilla, direccion):

    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            
            pos_actual = c, f

            if grilla[f][c] == JUGADOR:

                caracteres_a_cambiar = obtener_caracteres_a_cambiar(grilla, direccion, pos_actual, VACIO)

                return cambiar_contenido_celdas(grilla, direccion, caracteres_a_cambiar, pos_actual)

            if grilla[f][c] == OBJETIVO_Y_JUGADOR:

                caracteres_a_cambiar = obtener_caracteres_a_cambiar(grilla, direccion, pos_actual, OBJETIVO)

                return cambiar_contenido_celdas(grilla, direccion, caracteres_a_cambiar, pos_actual)