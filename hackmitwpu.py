#!/usr/bin/env python3

from csv import reader
from collections import defaultdict
from heapq import nlargest

import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'dead_entries.csv'

with open(filename, 'r') as file:
    data = list(reader(file))

scores = defaultdict(lambda: 0)

for row in data[1:]:
    try:
        scores[row[0]] += int(row[-1])
    except Exception as e:
        print(e)
        print(row)
        break

winners = nlargest(4, scores, key=scores.get)
for x in winners:
    print(f"{x} has a score of {scores[x]}")
