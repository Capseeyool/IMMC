import random
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

MODEL = 'steffen'
ROWS = 32
LOADING_TIME = {
    'times': [0, 1, 2, 3, 4, 5, 6],
    'weights': [1 for i in range(7)]
}

class Passenger:
    def __init__(self, column, row):
        self.column = column  # A B C D E F
        self.row = row  # 1-32

        self.seated = False
        self.timer = 0
    
    def __int__(self):
        return 1 if self.seated else 2
    
    def __repr__(self):
        return f'{self.column}{self.row}{"*" if self.seated else ""}'

grid = pd.DataFrame(np.array([[0 for i in range(7)] for i in range(ROWS)])).astype(object)
grid.columns = list('ABC DEF')
grid.index = range(1, ROWS + 1)[::-1]

figs = []

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticks(ticks=np.arange(7), labels=grid.columns)
ax.set_yticks(ticks=np.arange(ROWS), labels=grid.index)

all = [Passenger(i, j) for i in 'ABCFED' for j in range(ROWS, 0, -1)]

steffen = []
for k in ['AF', 'BE', 'CD']:
    for i in k:
        for j in range(ROWS, 0, -2):
            steffen.append(Passenger(i, j))
    for i in k:
        for j in range(ROWS-1, 0, -2):
            steffen.append(Passenger(i, j))

models = {
    'BTF': [Passenger(j, i) for i in range(ROWS, 0, -1) for j in 'ABCFED'],
    'FTB': [Passenger(j, i) for i in range(1, 33) for j in 'ABCFED'],
    'random': random.sample(all, ROWS * 6),
    'steffen': steffen,
    'test': [Passenger('C', 1), Passenger('B', 1), Passenger('A', 1)],
    'WMA': [Passenger(i, j) for i in 'ABCFED' for j in range(ROWS, 0, -1)],
    'WMArandom': [Passenger(i, j) for i in 'ABCFED' for j in random.sample(range(ROWS, 0, -1), ROWS)]
}
passengers = models[MODEL]
time = 0

while len(passengers) or sum(list(map(int, grid[' ']))) != 0:
    for i in ['B', 'E', 'C', 'D', ' ']:
        for j in grid.index:
            cur = grid[i][j]
            if cur == 0 or cur.seated:
                continue
            if cur.row == j:
                if i == 'B':
                    if grid['A'][j] == 0:
                        grid['A'][j] = cur
                        grid['A'][j].seated = True
                        grid[i][j] = 0
                    else:
                        temp = grid['A'][j]
                        grid['A'][j] = cur
                        grid[i][j] = temp
                        grid[i][j].seated = False
                elif i == 'E':
                    if grid['F'][j] == 0:
                        grid['F'][j] = cur
                        grid['F'][j].seated = True
                        grid[i][j] = 0
                    else:
                        temp = grid['F'][j]
                        grid['F'][j] = cur
                        grid[i][i] = temp
                        grid[i][j].seated = False
                elif i == 'C':
                    if grid['B'][j] == 0:
                        grid['B'][j] = cur
                        grid['B'][j].seated = True if cur.column == 'B' else False
                        grid[i][j] = 0
                    elif ord(cur.column) < ord(grid['B'][j].column):
                        temp = grid['B'][j]
                        grid['B'][j] = cur
                        grid[i][j] = temp
                        grid[i][j].seated = False
                elif i == 'D':
                    if grid['E'][j] == 0:
                        grid['E'][j] = cur
                        grid['E'][j].seated = True if cur.column == 'E' else False
                        grid[i][j] = 0
                    elif ord(cur.column) > ord(grid['E'][j].column):
                        temp = grid['E'][j]
                        grid['E'][j] = cur
                        grid[i][j] = temp
                        grid[i][j].seated = False
                else:
                    if cur.timer > 0:
                        grid[i][j].timer -= 1
                    else:
                        if cur.column in list('ABC'):
                            if grid['C'][j] == 0:
                                grid['C'][j] = cur
                                grid['C'][j].seated = True if cur.column == 'C' else False
                                grid[i][j] = 0
                            elif ord(cur.column) < ord(grid['C'][j].column):
                                temp = grid['C'][j]
                                grid['C'][j] = cur
                                grid[i][j] = temp
                                grid[i][j].seated = False
                        else:
                            if grid['D'][j] == 0:
                                grid['D'][j] = cur
                                grid['D'][j].seated = True if cur.column == 'D' else False
                                grid[i][j] = 0
                            elif ord(cur.column) > ord(grid['D'][j].column):
                                temp = grid['D'][j]
                                grid['D'][j] = cur
                                grid[i][j] = temp
                                grid[i][j].seated = False
            else:
                if grid[i][j + 1] == 0:
                    grid[i][j + 1] = cur
                    grid[i][j] = 0
                    if cur.row == j + 1:
                        grid[i][j + 1].timer = random.choices(LOADING_TIME['times'], LOADING_TIME['weights'])[0]
    if grid[' '][1] == 0:
        try:
            grid[' '][1] = passengers.pop(0)
            if grid[' '][1].row == 1:
                grid[' '][1].timer = random.choices(LOADING_TIME['times'], LOADING_TIME['weights'])[0]
        except IndexError:
            pass

    image = ax.imshow(np.array(grid, dtype=int))
    figs.append([image])
    time += 1

ani = anim.ArtistAnimation(fig, figs, interval=100)
ani.save(f'{MODEL}/{MODEL}.gif')
print(time)