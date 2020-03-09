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

judge_eval = defaultdict(lambda: dict())

for row in data[1:]:
    try:
        team = row[2]
        judge = row[1]
        if judge not in judge_eval[team].keys():
            judge_eval[team][judge] = sum(map(int, row[3:]))
        else:
            print(f"repeated row for judge {judge} and team {team}")
    except Exception as e:
        print(e)
        print(row)
        break

scores = dict()
for team in judge_eval.keys():
    scores[team] = sum(judge_eval[team].values()) / len(judge_eval[team].values())

winners = nlargest(len(scores.items()), scores, key=scores.get)

print()
for x in winners:
    print(f"{x} has a score of {scores[x]}")
