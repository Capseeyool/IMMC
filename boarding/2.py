import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROWS = 32

class Passenger:
    def __init__(self, section, row, column):
        self.section = section
        self.row = row
        self.column = column

        self.seated = False
        self.timer = 0

plane = pd.DataFrame(np.zeros([ROWS + 1, 28])).astype(object)
plane.columns = [f'{i}{j}' for i in 'ABCD' for j in 'ABC DEF']
plane.index = range(ROWS + 1)[::-1]
print(plane)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticks(ticks=np.arange(28), labels=plane.columns)
ax.set_yticks(ticks=np.arange(ROWS + 1), labels=plane.index)

figs = []

image = ax.imshow(np.array(plane, dtype=int))
figs.append([image])