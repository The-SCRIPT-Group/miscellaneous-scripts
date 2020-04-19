#!/usr/bin/env python3

import csv
import os

from mail import send_certificate

with open("../event-csv/ranksortedfinal.csv") as participants_file:
    participants = csv.reader(participants_file, delimiter=",")
    for row in participants:
        cert_file = f'../Certificates/Battle-of-Vars/{row[6]}.jpg'
        if os.path.exists(cert_file):
            send_certificate(row[1], row[2], cert_file, row[6])
