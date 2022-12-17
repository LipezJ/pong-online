import random as rn
import os
import time
import curses
from curses import wrapper
from pytimedinput import timedKey
import socketio

def imprimir_tablero(stdscr, nuevo, actual_rows1, actual_rows2,puntos):
    stdscr.addstr('x'*(tablero[1]+1) + f'\n')
    for row in range(tablero[0]):
        if row == actual_rows1[0] or row == actual_rows1[1]:
            stdscr.addstr('|')
        else:
            stdscr.addstr(' ')
        if nuevo[0] == row:
            stdscr.addstr((' '*(nuevo[1])) + 'O' + ' '*(tablero[1]-(nuevo[1]+1)))
        else:
            stdscr.addstr(' '*(tablero[1]))
        if row == actual_rows2[0] or row == actual_rows2[1]:
            stdscr.addstr('|')
        else:
            stdscr.addstr(' ')
        stdscr.addstr(f'\n')
    stdscr.addstr('x'*(tablero[1]+1))
    stdscr.addstr(f'\n {puntos[0]} - {puntos[1]}')

def posibilidades_(actual):
    if (actual[0] == 0 and actual[1] == 0) or (actual[0] == 0 and actual[1] == tablero[1]-1) or (actual[0] == tablero[0]-1 and actual[1] == 0) or (actual[0] == tablero[0]-1 and actual[1] == tablero[1]-1):
        return [4]
    if actual[0] == tablero[0]-1:
        posibilidades_ = [0, 1]
    elif actual[0] == 0:
        posibilidades_ = [2, 3]
    elif actual[1] == tablero[1]-1:
        posibilidades_ = [0, 3]
    elif actual[1] == 0:
        posibilidades_ = [1, 2]
    else:
        posibilidades_ = [0,1,2,3]
    return posibilidades_

tablero = [15, 50]
rows = tablero[0]
movimientos = {
    0: [-1, -1], 1: [-1, 1], 
    2: [1, 1], 3: [1, -1]
}
movimientos_ = {
    "-1-1": 0, "-11": 1,
    "1-1": 3, "11": 2,
    "00": 4
}
movimientos__ = {0: 2, 1: 3, 2: 0, 3: 1}
movimientos_area = {'w': -1, 'd': 1}

url = input("url: ")
if len(url) < 10: url = "http://localhost:3000"

response = [0,[0,0],0,[0,0]]
sio = socketio.Client()
sio.connect(url)

@sio.on('cget')
def cget(data):
    global response
    response = data

party = input('igrese el nombre de la party: ')
os.system(f'mode con: cols={tablero[1]+3} lines={tablero[0]+4}')

def main(stdscr):

    actual_rows1 = [rows//2, rows//2+1]
    actual_rows2 = [rows//2, rows//2+1]
    nuevo = [rn.randint(0, tablero[0]-1), tablero[1]//2]
    actual = nuevo
    puntos = [0, 0]

    while True:
        stdscr.clear()
        #teclas
        key, timeout = timedKey(allowCharacters='wdq', timeout=0.03, toprint=False)
        if key == 'q':
            sio.disconnect()
            return 0

        anterior = actual
        actual = nuevo

        #calcular el tipo de movimiento anterior
        tipo = movimientos_[str(actual[0] - anterior[0]) + str(actual[1] - anterior[1])]
        #ejecutar la funcion para saber cuantas posibilidades hay en el movimiento
        posibilidades = posibilidades_(actual)

        if not timeout:
            if (key == 'w' and actual_rows1[0] > 0) or (key == 'd' and actual_rows1[1] < rows-1):
                actual_rows1 = [ actual_rows1[0] + movimientos_area[key], actual_rows1[1] + movimientos_area[key]]
            time.sleep(0.055)
        else:
            time.sleep(0.03)

        if 10 in puntos:
            if puntos[0] == 10: print(f'\n Ganaste! jugador 1 \n')
            else: print(f'\n Ganaste! jugador 2 \n')
            time.sleep(1)
            return 0
            
        #primer movimiento
        if actual == anterior:
            posibilidad = rn.choice(posibilidades)
            nuevo = [actual[0] + (movimientos[posibilidad][0]), actual[1] + (movimientos[posibilidad][0])]
        #esquinas
        elif posibilidades[0] == 4:
            if  actual[0] == actual_rows1[0] or actual[0] == actual_rows1[1] or actual_rows2[0] == actual[0] or actual_rows2[1] == actual[0]:
                nuevo = anterior
            elif not (actual_rows1[0] == actual[0] or actual_rows1[1] == actual[0]):
                nuevo = [rn.randint(0, tablero[0]-1), tablero[1]//2]
                actual = nuevo
                puntos[1] += 1
            elif not (actual_rows2[0] == actual[0] or actual_rows2[1] == actual[0]):
                nuevo = [rn.randint(0, tablero[0]-1), tablero[1]//2]
                actual = nuevo
                puntos[0] += 1
        #movimientto normal
        elif len(posibilidades) == 4:
            nuevo = [actual[0] + (actual[0] - anterior[0]), actual[1] + (actual[1] - anterior[1])]

        elif posibilidades == [1, 2] and not (actual_rows1[0] == actual[0] or actual_rows1[1] == actual[0]):
            nuevo = [rn.randint(0, tablero[0]-1), tablero[1]//2]
            actual = nuevo
            puntos[1] += 1
        elif posibilidades == [0, 3] and not (actual_rows2[0] == actual[0] or actual_rows2[1] == actual[0]):
            nuevo = [rn.randint(0, tablero[0]-1), tablero[1]//2]
            actual = nuevo
            puntos[0] += 1

        #rebotes
        else:
            if posibilidades == [1, 2]:
                if actual_rows1[0] == actual[0]:
                    tipo = 0
                elif actual_rows1[1] == actual[0]:
                    tipo = 3
            if posibilidades == [0, 3]:
                if actual_rows2[1] == actual[0]:
                    tipo = 1
                elif actual_rows2[0] == actual[0]:
                    tipo = 2
            posibilidades.remove(movimientos__[tipo])
            nuevo = [actual[0] + movimientos[posibilidades[0]][0], actual[1] + movimientos[posibilidades[0]][1]]
        
        sio.emit('seth', {"name": party, "posr": actual_rows1[0], "pos": actual, "points": puntos})
        sio.emit('get', {"name": party})

        actual_rows2 = [response[2], response[2]-1]

        imprimir_tablero(stdscr, nuevo, actual_rows1, actual_rows2, puntos)
        stdscr.refresh()

wrapper(main)
sio.disconnect()