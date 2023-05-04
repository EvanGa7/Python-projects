# roster_fields.py - Read the contents of cs176roster.webadvisor.txt and write the contents to roster.txt using a for loop
# Evan Gardner
# 1270495
# CS-171
# Spring 2023

with open("cs176roster.webadvisor.txt", "r") as roster:
    lines = roster.readlines()

with open("roster.txt", "w") as roster_output:
    for i in range(0, len(lines), 8):
        name = lines[i].strip()
        student_id = lines[i+1].strip()
        email = lines[i+2].strip()
        major = lines[i+3].strip()
        year = lines[i+4].strip()
        advisor = lines[i+5].strip()
        gpa = lines[i+6].strip()
        roster_output.write(", ".join((name, student_id, major, year, advisor, gpa)) + "\n")
