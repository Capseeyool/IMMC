import csv
import os
from simulation import simulation

MODEL = 'WMArandom'
PERCENTAGE = 0

times = []

for i in range(1000):
    print(i)
    times.append(simulation(MODEL, PERCENTAGE))

if not os.path.exists(f'{MODEL}{PERCENTAGE}'):
    os.mkdir(f'{MODEL}{PERCENTAGE}')

with open(f'{MODEL}{PERCENTAGE}/{MODEL}{PERCENTAGE}.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(times)