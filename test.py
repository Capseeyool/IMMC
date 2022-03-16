import numpy as np
import pandas as pd

plane = pd.DataFrame(np.zeros([32, 7])).astype(object)
plane.columns = list('ABC DEF')
plane.index = range(1, 32 + 1)[::-1]

print(plane)