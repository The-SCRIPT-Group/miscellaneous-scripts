from csv import reader
from collections import defaultdict
from heapq import nlargest

with open('dead_entries.csv', 'r') as file:
    data = list(reader(file))

scores = defaultdict(lambda: 0)

for row in data[1:]:
    try:
        scores[row[2]] += int(row[6])
    except Exception as e:
        print(e)
        print(row)
        break

winners = nlargest(4, scores, key=scores.get)
for x in winners:
    print(x, scores[x])
