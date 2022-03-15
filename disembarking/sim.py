import csv
from simulation import simulation

times = []

for i in range(1000):
    print(i)
    times.append(simulation())

with open('disembarking.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(times)