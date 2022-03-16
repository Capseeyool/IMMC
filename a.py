import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticks(ticks=np.arange(7), labels=list('ABC DEF'))
ax.set_yticks(ticks=np.arange(32), labels=range(32, 0, -1))
image = ax.imshow(np.zeros([32, 7]))
plt.savefig('empty.png')
plt.show()