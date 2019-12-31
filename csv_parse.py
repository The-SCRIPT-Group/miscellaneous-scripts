#!/usr/bin/env python3
import csv

with open("Participants.csv") as participants_file:
    participants = csv.reader(participants_file, delimiter=",")
    for row in participants:
        attendance = open("CodexAttendance.csv")
        attended = csv.reader(attendance, delimiter="|")
        for person in attended:
            names = [name.strip() for name in person[0].split(",")]
            if len(names) == 1:
                if names[0] == row[0]:
                    print(f"{row[0]} with id {row[3]} has email {person[1]}.")
                    break
            else:
                if row[0] == names[0]:
                    print(
                        f"{row[0]} with id {row[3]} has email {person[1].split(',')[0].strip()}."
                    )
                    break
                elif row[0] == names[1]:
                    print(
                        f"{row[0]} with id {row[3]} has email {person[1].split(',')[1].strip()}."
                    )

                    break
        attendance.close()
