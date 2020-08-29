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

headers['User-Agent'] = 'db-dump/1.0'

tables = (
    get('https://hades.thescriptgroup.in/api/events', headers=headers).json().keys()
)

for table in tables:
    params = {'table': table}

    response = get(
        'https://hades.thescriptgroup.in/api/users', headers=headers, params=params
    )

    if response.status_code != 200:
        try:
            print(response.json()['message'])
        except:
            print(response.text)
        exit(1)

    users = response.json()

    with open(f'{table}.csv', 'w') as f:
        for user in users:
            for field in user.keys():
                f.write(f'{user[field]},')
            f.write('\n')
