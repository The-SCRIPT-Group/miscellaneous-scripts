#!/usr/bin/env python3

from base64 import b64encode
from datetime import datetime
from getpass import getpass
from requests import get
from os import getenv

GITHUB_OAUTH_TOKEN = getenv("GITHUB_OAUTH_TOKEN")
HADES_API_KEY = getenv("HADES_API_KEY")
ORGANIZATION = "The-SCRIPT-Group"
repos = []

if GITHUB_OAUTH_TOKEN is None:
    GITHUB_OAUTH_TOKEN = input(
        "Enter your Github API token or try without one, which may result in you getting rate-limited soon: "
    )


headers = {"Authorization": "token " + GITHUB_OAUTH_TOKEN}

since = datetime.strptime("1 Jan 2019", "%d %b %Y")
until = datetime.strptime("1 Jan 2020", "%d %b %Y")

data = {
    "since": since.isoformat(),
    "until": until.isoformat(),
}

EMAILS = {
    "Aditya Desai": (
        "aditya.desai0199@gmail.com",
        "AdityaDesai-99@users.noreply.github.com",
    ),
    "Akhil Narang": (
        "akhilnarang.1999@gmail.com",
        "akhilnarang@thescriptgroup.in",
        "me@akhilnarang.dev",
    ),
    "Aniket Inamdar": (
        "50190428+aniket1020@users.noreply.github.com",
        "aniket.1020@gmail.com",
    ),
    "Aniket Raj": (
        "aniketronaldo10@gmail.com",
        "aniket-spidey@users.noreply.github.com",
    ),
    "Anunay Maheshwari": ("anunaymaheshwari@thescriptgroup.in", "anunaym14@gmail.com"),
    "Kshitish Deshpande": ("ksdfg123@gmail.com", "ksdfg@users.noreply.github.com"),
    "Omkar Chandorkar": (
        "forumomkar@gmail.com",
        "37974264+gotenksIN@users.noreply.github.com",
    ),
    "Pranav Bakre": (
        "43286669+PranavBakre@users.noreply.github.com",
        "psbakre@yahoo.com",
    ),
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


if HADES_API_KEY is not None:
    headers = {"Authorization": HADES_API_KEY}
else:
    headers = {
        "Credentials": b64encode(
            str(
                input("Enter your Hades username: ")
                + "|"
                + getpass(prompt="Enter your Hades password: ")
            ).encode()
        )
    }

response = get("https://hades.thescriptgroup.in/api/stats", headers=headers).json()

print()

event_count, registrations_count = 0, 0
for event in response:
    print(f"{event} - {response[event]}")
    event_count += 1
    registrations_count += response[event]

print()

print(f"Number of events - {event_count}")
print(f"Number of registrations - {registrations_count}")
