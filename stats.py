#!/usr/bin/env python3

from datetime import datetime
from requests import get
from os import getenv

GITHUB_OAUTH_TOKEN = getenv("GITHUB_OAUTH_TOKEN")
ORGANIZATION = "The-SCRIPT-Group"
repos = []

headers = {
    "Authorization": "token " + GITHUB_OAUTH_TOKEN
    if GITHUB_OAUTH_TOKEN is not None
    else input("Enter your Github API token: ")
}

since = datetime.strptime("1 Jan 2019", "%d %b %Y")
until = datetime.strptime("1 Jan 2020", "%d %b %Y")

data = {
    "since": since.isoformat(),
    "until": until.isoformat(),
}

EMAILS = {
    "Aditya Desai": (
        "aditya.desai0199@gmail.com",
        "adityadesai-99@users.noreply.github.com",
    ),
    "Akhil Narang": ("akhilnarang.1999@gmail.com", "akhilnarang@thescriptgroup.in"),
    "Aniket Raj": (
        "aniketronaldo10@gmail.com",
        "aniket-spidey@users.noreply.github.com",
    ),
    "Kshitish Deshpande": ("ksdfg123@gmail.com", "ksdfg@users.noreply.github.com"),
    "Ritom Gupta": ("ritomgupta99@gmail.com", "rightonrittman@gmail.com"),
}


def get_author(commit):
    for name, emails in EMAILS.items():
        for email in emails:
            if email in commit["commit"]["author"]["email"]:
                return name
    return (
        commit["commit"]["author"]["name"]
        + " "
        + "<"
        + commit["commit"]["author"]["email"]
        + ">"
    )


response = get(f"https://api.github.com/orgs/{ORGANIZATION}/repos", headers=headers)
while True:
    for repo in response.json():
        repos.append(repo["name"])
    try:
        response = get(response.links["next"]["url"], headers=headers)
    except KeyError:
        break


commits, total_commits = 0, 0

authors = {}

for repo in repos:
    response = get(
        f"https://api.github.com/repos/{ORGANIZATION}/{repo}/commits",
        headers=headers,
        data=data,
    )
    while True:
        commits += len(response.json())
        for commit in response.json():
            author = get_author(commit)
            if author not in authors.keys():
                authors[author] = 1
            else:
                authors[author] += 1
        try:
            response = get(response.links["next"]["url"], headers=headers, data=data)
        except KeyError:
            break
    print(f"{repo} - {commits}")
    total_commits += commits
    commits = 0

print(
    f"Total commits in {ORGANIZATION} from {since.strftime('%d %B %Y')} until {until.strftime('%d %B %Y')}  is {total_commits}!"
)
print("*" * 80)
print("Commits per person: ")
print()
for author in authors:
    print(f"{author} - {authors[author]}")
