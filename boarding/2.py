import random
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from time import sleep

ROWS = 32
# LOADING_TIME = {
#     'times': [6, 7, 8, 9],
#     'weights': [1 for i in range(4)]
# }
LOADING_TIME = {
    'times': [3],
    'weights': [1]
}

class Passenger:
    def __init__(self, section, row, column):
        self.section = section
        self.row = row
        self.column = column

        self.seated = False
        self.timer = 0

    def __int__(self):
        return 1 if self.seated else 2
    
    def __repr__(self):
        return f'{self.section}{self.row}{self.column}{"*" if self.seated else ""}'

plane = pd.DataFrame(np.zeros([ROWS + 1, 28])).astype(object)
plane.columns = [f'{i}{j}' for i in 'ABCD' for j in 'ABC DEF']
plane.index = range(ROWS + 1)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticks(ticks=np.arange(28), labels=plane.columns)
ax.set_yticks(ticks=np.arange(ROWS + 1), labels=plane.index)

figs = []

image = ax.imshow(np.array(plane, dtype=int))
figs.append([image])

all = []
for section in 'DCBA':
    for row in range(32, 0, -1):
        for column in 'ABCFED':
            all.append(Passenger(section, row, column))

passengers = all

frames = 0

while len(passengers) or plane.loc[0].astype(int).sum() or plane['A '].astype(int).sum() or plane['B '].astype(int).sum() or plane['C '].astype(int).sum() or plane['D '].astype(int).sum():
    for section in 'ABCD':
        for column in 'BECD ':
            for row in range(ROWS, 0, -1):
                cur = plane[f'{section}{column}'][row]
                if cur == 0 or cur.seated:
                    continue
                if cur.row == row:
                    if column == 'B':
                        plane[f'{section}A'][row] = cur
                        plane[f'{section}A'][row].seated = True
                        plane[f'{section}B'][row] = 0
                    elif column == 'E':
                        plane[f'{section}F'][row] = cur
                        plane[f'{section}F'][row].seated = True
                        plane[f'{section}E'][row] = 0
                    elif column == 'C':
                        if plane[f'{section}B'][row] == 0:
                            plane[f'{section}B'][row] = cur
                            plane[f'{section}B'][row].seated = True if cur.column == 'B' else False
                            plane[f'{section}C'][row] = 0
                        elif ord(cur.column) < ord(plane[f'{section}B'][row].column):
                            temp = plane[f'{section}B'][row]
                            plane[f'{section}B'][row] = cur
                            plane[f'{section}C'][row] = temp
                            plane[f'{section}C'][row].seated = False
                    elif column == 'D':
                        if plane[f'{section}E'][row] == 0:
                            plane[f'{section}E'][row] = cur
                            plane[f'{section}E'][row].seated = True if cur.column == 'E' else False
                            plane[f'{section}D'][row] = 0
                        elif ord(cur.column) > ord(plane[f'{section}E'][row].column):
                            temp = plane[f'{section}E'][row]
                            plane[f'{section}E'][row] = cur
                            plane[f'{section}D'][row] = temp
                            plane[f'{section}D'][row].seated = False
                    elif column == ' ':
                        if cur.timer:
                            plane[f'{section} '][row].timer -= 1
                        else:
                            if cur.column in list('ABC'):
                                if plane[f'{section}C'][row] == 0:
                                    plane[f'{section}C'][row] = cur
                                    plane[f'{section}C'][row].seated = True if cur.column == 'C' else False
                                    plane[f'{section} '][row] = 0
                                elif ord(cur.column) < ord(plane[f'{section}C'][row].column):
                                    temp = plane[f'{section}C'][row]
                                    plane[f'{section}C'][row] = cur
                                    plane[f'{section} '][row] = temp
                                    plane[f'{section} '][row].seated = False
                            else:
                                if plane[f'{section}D'][row] == 0:
                                    plane[f'{section}D'][row] = cur
                                    plane[f'{section}D'][row].seated = True if cur.column == 'D' else False
                                    plane[f'{section} '][row] = 0
                                elif ord(cur.column) > ord(plane[f'{section}D'][row].column):
                                    temp = plane[f'{section}D'][row]
                                    plane[f'{section}D'][row] = cur
                                    plane[f'{section} '][row] = temp
                                    plane[f'{section} '][row].seated = False
                else:
                    if plane[f'{section} '][row + 1] == 0:
                        plane[f'{section} '][row + 1] = cur
                        plane[f'{section} '][row] = 0
                        if cur.row == row + 1:
                            plane[f'{section} '][row + 1].timer = random.choices(LOADING_TIME['times'], LOADING_TIME['weights'])[0]
    
    c = plane.columns[:-1][::-1]

    for i, v in enumerate(c):
        cur = plane[v][0]
        if cur == 0:
            continue
        if v[1] == ' ':
            if plane[v][0].section == v[0]:
                if plane[v][1] == 0:
                    plane[v][1] = cur
                    if cur.row == 1:
                        plane[v][1].timer = random.choices(LOADING_TIME['times'], LOADING_TIME['weights'])[0]
                    plane[v][0] = 0
            elif plane[c[i - 1]][0] == 0:
                plane[c[i - 1]][0] = cur
                plane[v][0] = 0
        elif plane[c[i - 1]][0] == 0:
            plane[c[i - 1]][0] = cur
            plane[v][0] = 0
    
    if plane['AA'][0] == 0:
        try:
            plane['AA'][0] = passengers.pop(0)
        except IndexError:
            pass
    
    image = ax.imshow(np.array(plane, dtype=int))
    figs.append([image])
    frames += 1

ani = anim.ArtistAnimation(fig, figs, interval=10)
ani.save(f'test/test.gif')
print(frames)