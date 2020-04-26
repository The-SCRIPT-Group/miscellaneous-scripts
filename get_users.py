#!/usr/bin/env python3

from base64 import b64encode
from getpass import getpass
from requests import get
from os import getenv
from sys import exit

HADES_API_KEY = getenv('HADES_API_KEY')

if HADES_API_KEY is not None:
    headers = {'Authorization': HADES_API_KEY}
else:
    headers = {
        'Credentials': b64encode(
            str(
                input('Enter your Hades username: ')
                + '|'
                + getpass(prompt='Enter your Hades password: ')
            ).encode()
        )
    }

params = {'table': input('Enter table name: ')}

start = int(input('Enter the starting entry number: '))
end = int(input('Enter the ending entry number: '))
count = 0

response = get(
    'https://hades.thescriptgroup.in/api/users', headers=headers, params=params
)

if response.status_code != 200:
    print(response.json()['response'])
    exit(1)

users = response.json()

print('fullname,email')
for user in users:
    count += 1
    if count >= start and count <= end:
        print(user['name'] + ',' + user['email'])
