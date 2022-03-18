import csv
import os
from simulation2 import simulation

times = []

for i in range(100):
    print(i)
    times.append(simulation())

if not os.path.exists('test'):
    os.mkdir('test')

with open('test/test.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(times)