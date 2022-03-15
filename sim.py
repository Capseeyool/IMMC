import csv
from simulation import simulation

MODEL = 'WMA'

times = []

for i in range(1000):
    print(i)
    times.append(simulation(MODEL))

with open(f'{MODEL}/{MODEL}.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(times)