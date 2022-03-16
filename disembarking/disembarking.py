import random
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROWS = 32
# LOADING_TIME = {
#     'times': [0, 1, 2, 3, 4, 5, 6],
#     'weights': [1 for i in range(7)]
# }
LOADING_TIME = {
    'times' : [3],
    'weights': [1]
}

class Passenger:
    def __init__(self, column, row):
        self.column = column  # A B C D E F
        self.row = row  # 1-32

        self.timer = 0
    
    def __int__(self):
        return 4 - self.timer
    
    def __repr__(self):
        return f'{self.column}{self.row}'

grid = pd.DataFrame(np.zeros([ROWS, 7])).astype(object)
grid.columns = list('ABC DEF')
grid.index = range(1, ROWS + 1)[::-1]
for i in 'ABCDEF':
    for j in grid.index:
        grid[i][j] = Passenger(i, j)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticks(ticks=np.arange(7), labels=grid.columns)
ax.set_yticks(ticks=np.arange(ROWS), labels=grid.index)

figs = []

image = ax.imshow(np.array(grid, dtype=int))
figs.append([image])

time = 0

while np.array(grid, dtype=int).sum():
    if grid[' '][1]:
        if grid[' '][1].timer == 0:
            grid[' '][1] = 0
    for i in ' CDBEAF':
        for j in grid.index[::-1]:
            cur = grid[i][j]
            if cur == 0:
                continue
            if i == ' ':
                if cur.timer:
                    grid[i][j].timer -= 1
                    continue
                if j == 1:
                    continue
                elif grid[i][j - 1] == 0:
                    grid[i][j - 1] = cur
                    grid[i][j] = 0
            elif i in list('CD'):
                if grid[' '][j] == 0:
                    grid[' '][j] = cur
                    grid[' '][j].timer = random.choices(LOADING_TIME['times'], LOADING_TIME['weights'])[0]
                    grid[i][j] = 0
            elif i == 'B':
                if grid['C'][j] == 0:
                    grid['C'][j] = cur
                    grid[i][j] = 0
            elif i == 'E':
                if grid['D'][j] == 0:
                    grid['D'][j] = cur
                    grid[i][j] = 0
            elif i == 'A':
                if grid['B'][j] == 0:
                    grid['B'][j] = cur
                    grid[i][j] = 0
            elif i == 'F':
                if grid['E'][j] == 0:
                    grid['E'][j] = cur
                    grid[i][j] = 0

    image = ax.imshow(np.array(grid, dtype=int))
    figs.append([image])
    time += 1

ani = anim.ArtistAnimation(fig, figs, interval=100)
ani.save('disembarking.gif')
print(time)