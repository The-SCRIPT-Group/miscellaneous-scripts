#!/usr/bin/env python

from requests import get

contest_name = "battle-of-vars-2020"

# For some reason hackerrank API seemed to work fine with cURL's user-agent
# With request's default user-agent, it was throwing us an access denied
headers = {"user-agent": "curl/7.69.1"}

count = 0
total = 0

print("srno,username,rank,score,country")
while True:
    response = get(
        f"https://www.hackerrank.com/rest/contests/{contest_name}/leaderboard?limit=100&offset={count}",
        allow_redirects=True,
        headers=headers,
    )
    data = response.json()
    if total == 0:
        total = data["total"]
    for model in data["models"]:
        count += 1
        print(
            f"{count},{model['hacker']},{model['rank']},{model['score']},{model['country']}"
        )

    if total != 0 and count == total:
        break
