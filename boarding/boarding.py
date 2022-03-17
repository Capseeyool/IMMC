import random
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

MODEL = 'WMArandom'
PERCENTAGE = 0
# LOADING_TIME = {
#     'times': [0, 1, 2, 3, 4, 5, 6],
#     'weights': [1 for i in range(7)]
# }
LOADING_TIME = {
    'times': [6, 7, 8, 9],
    'weights': [1 for i in range(4)]
}
ROWS = 32

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

plane = pd.DataFrame(np.zeros([ROWS, 7])).astype(object)
plane.columns = list('ABC DEF')
plane.index = range(1, ROWS + 1)[::-1]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticks(ticks=np.arange(7), labels=plane.columns)
ax.set_yticks(ticks=np.arange(ROWS), labels=plane.index)

figs = []

image = ax.imshow(np.array(plane, dtype=int))
figs.append([image])

all = [Passenger(i, j) for i in 'ABCDEF' for j in plane.index]
bow = [Passenger(i, j) for i in 'ABCDEF' for j in range(1, 12)]
middle = [Passenger(i, j) for i in 'ABCDEF' for j in range(12, 22)]
aft = [Passenger(i, j) for i in 'ABCDEF' for j in range(22, 33)]

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
    'sectionBTF': random.sample(aft, len(aft)) + random.sample(middle, len(middle)) + random.sample(bow, len(bow)),
    'sectionFTB': random.sample(bow, len(bow)) + random.sample(middle, len(middle)) + random.sample(aft, len(aft)),
    'steffen': steffen,
    'WMA': [Passenger(i, j) for i in 'ABCFED' for j in range(ROWS, 0, -1)],
    'WMArandom': [Passenger(i, j) for i in 'ABCFED' for j in random.sample(range(ROWS, 0, -1), ROWS)]
}

passengers = models[MODEL]

for i in range(PERCENTAGE*len(passengers)//100):
    temp = passengers.pop(random.randint(1, len(passengers) - 1))
    passengers.insert(random.randint(1, len(passengers) - 1), temp)

frames = 0

while len(passengers) or sum(list(map(int, plane[' ']))) != 0:
    for i in 'BECD ':
        for j in plane.index:
            cur = plane[i][j]
            if cur == 0 or cur.seated:
                continue
            if cur.row == j:
                if i == 'B':
                    plane['A'][j] = cur
                    plane['A'][j].seated = True
                    plane[i][j] = 0
                elif i == 'E':
                    plane['F'][j] = cur
                    plane['F'][j].seated = True
                    plane[i][j] = 0
                elif i == 'C':
                    if plane['B'][j] == 0:
                        plane['B'][j] = cur
                        plane['B'][j].seated = True if cur.column == 'B' else False
                        plane[i][j] = 0
                    elif ord(cur.column) < ord(plane['B'][j].column):
                        temp = plane['B'][j]
                        plane['B'][j] = cur
                        plane[i][j] = temp
                        plane[i][j].seated = False
                elif i == 'D':
                    if plane['E'][j] == 0:
                        plane['E'][j] = cur
                        plane['E'][j].seated = True if cur.column == 'E' else False
                        plane[i][j] = 0
                    elif ord(cur.column) > ord(plane['E'][j].column):
                        temp = plane['E'][j]
                        plane['E'][j] = cur
                        plane[i][j] = temp
                        plane[i][j].seated = False
                elif i == ' ':
                    if cur.timer:
                        plane[i][j].timer -= 1
                    else:
                        if cur.column in list('ABC'):
                            if plane['C'][j] == 0:
                                plane['C'][j] = cur
                                plane['C'][j].seated = True if cur.column == 'C' else False
                                plane[i][j] = 0
                            elif ord(cur.column) < ord(plane['C'][j].column):
                                temp = plane['C'][j]
                                plane['C'][j] = cur
                                plane[i][j] = temp
                                plane[i][j].seated = False
                        else:
                            if plane['D'][j] == 0:
                                plane['D'][j] = cur
                                plane['D'][j].seated = True if cur.column == 'D' else False
                                plane[i][j] = 0
                            elif ord(cur.column) > ord(plane['D'][j].column):
                                temp = plane['D'][j]
                                plane['D'][j] = cur
                                plane[i][j] = temp
                                plane[i][j].seated = False
            else:
                if plane[i][j + 1] == 0:
                    plane[i][j + 1] = cur
                    plane[i][j] = 0
                    if cur.row == j + 1:
                        plane[i][j + 1].timer = random.choices(LOADING_TIME['times'], LOADING_TIME['weights'])[0]
    if plane[' '][1] == 0:
        try:
            plane[' '][1] = passengers.pop(0)
            if plane[' '][1].row == 1:
                plane[' '][1].timer = random.choices(LOADING_TIME['times'], LOADING_TIME['weights'])[0]
        except IndexError:
            pass

    image = ax.imshow(np.array(plane, dtype=int))
    figs.append([image])
    frames += 1

ani = anim.ArtistAnimation(fig, figs, interval=100)
ani.save(f'{MODEL}/{MODEL}.gif')
print(frames)