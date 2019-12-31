#!/usr/bin/env python3
import csv

with open("Participants.csv") as participants_file:
    participants = csv.reader(participants_file, delimiter=",")
    for row in participants:
        attendance = open("CodexAttendance.csv")
        attended = csv.reader(attendance, delimiter="|")
        for person in attended:
            names = [name.strip() for name in person[0].split(",")]
            if row[0] not in names:
                continue
            for name, email in zip(names, person[1].split(",")):
                if name == row[0]:
                    print(f"{row[0]} with id {row[3]} has email {email.strip()}.")
        attendance.close()
