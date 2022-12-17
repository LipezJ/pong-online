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
movimientos_area = {'k': -1, 'm': 1}

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

    actual_rows2 = [rows//2, rows//2+1]

    while True:
        stdscr.clear()

        #teclas
        key, timeout = timedKey(allowCharacters='qkm', timeout=0.03, toprint=False)
        if key == 'q':
            sio.disconnect()
            return 0

        if not timeout:
            if (key == 'k' and actual_rows2[0]) > 0 or (key == 'm' and actual_rows2[1] < rows-1):
                actual_rows2 = [ actual_rows2[0] + movimientos_area[key], actual_rows2[1] + movimientos_area[key]]
                sio.emit('setg', {"name": party, "pos": actual_rows2[1]})
            time.sleep(0.053)
        else:
            time.sleep(0.028)

        if 10 in response[3]:
            if response[3] == 10: print(f'\n Ganaste! jugador 1 \n')
            else: print(f'\n Ganaste! jugador 2 \n')
            time.sleep(1)
            return 0

        sio.emit('get', {"name": party})

        imprimir_tablero(stdscr, response[1], [response[0], response[0]+1], actual_rows2, response[3])

        stdscr.refresh()

wrapper(main)
sio.disconnect()