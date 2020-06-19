#!/usr/bin/env python3

from os import getenv
from os.path import join
from requests import get
from sys import exit

SENDGRID_API_KEY = getenv('SENDGRID_API_KEY')

if not SENDGRID_API_KEY:
    print('Please set the environment variable `SENDGRID_API_KEY`')
    exit(1)

headers = {'Authorization': f'Bearer {SENDGRID_API_KEY}'}

base_url = 'https://api.sendgrid.com/v3'
endpoint = 'email_activity'
events = 'delivered'

users = []
response = get(join(base_url, endpoint), headers=headers, params={'events': events})
while True:
    if 'errors' in response.json():
        print('-' * 100, 'ERROR', response.json()['errors'], '-' * 100, sep='\n')
        break
    for user in response.json():
        users.append(user['email'])
    try:
        response = get(response.links["next"]["url"], headers=headers)
    except KeyError:
        break

print(*users, sep='\n')
