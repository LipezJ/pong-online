#librerias
from pytimedinput import timedKey
import random as rn
import os
import time
import requests

#variables
tablero = [[0 for b in range(40)] for a in range(12)]
area2 = [0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0]

def imprimir():
    os.system('cls')
    for i in range(len(tablero[0])+1):
        print('x', end='')
    print()
    for i in range(len(area2)):
        response = requests.get(f'http://localhost:3000/get/{party}', data={}).json()
        if i == response[0] or i-1 == response[0]:
            print('|', end='')
        else:
            print(' ', end='')
        for j in range(len(tablero[0])):
            if i == response[1][0] and j == response[1][1]:
                print('O', end='')
            elif j == centro:
                print('|', end='')
            else:
                print(' ', end='')
        if area2[i] == '|':
            print(area2[i], end='')
            requests.post(f'http://localhost:3000/setg/{party}/{i}', data={})
        else:
            print(' ', end='')
        print()
    for i in range(len(tablero[0])+1):
        print('x', end='')
    print()
    print('puntos: ', puntos, ' - ', puntos2)

def mover2():
    nuevo_area2 = [
        actual_area2[0] + movimientos_area[key], 
        actual_area2[1] + movimientos_area[key]
    ]
    area2[actual_area2[0]] = 0
    area2[actual_area2[1]] = 0  
    area2[nuevo_area2[0]] = '|'
    area2[nuevo_area2[1]] = '|'

os.system("mode con: cols=42 lines=20")
centro = (len(tablero[0])-1)//2
movimientos_area = {'w': -1, 'd': 1, 'k': -1, 'm': 1}

puntos, puntos2 = 0, 0
party = input("ingrese el nombre de la party: ")

while(True):
    actual_area2 = [area2.index('|')]
    actual_area2.append(actual_area2[0]+1)
    key, timeout = timedKey(allowCharacters='qkm', timeout=0.1)
    if key == 'q':
        break
    if not timeout:
        if (key == 'k' and actual_area2[0] > 0) or (key == 'm' and actual_area2[1] < len(area2)-1):
            mover2()
        time.sleep(0.05)
    time.sleep(0.02)
    imprimir()