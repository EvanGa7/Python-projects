# roster_fields_re.py - Read the contents of cs176roster.webadvisor.txt and write the contents to roster.txt using regular expressions
# Evan Gardner
# 1270495
# CS-171
# Spring 2023

import re

with open("cs176roster.webadvisor.txt", "r") as roster:
    content = roster.read()

pattern = r'^([\w\s]+), ([\w\s]+(?:\s\w\.)?)\n(\d+)\n([\w\d@.]+)\n(\w{2,3})\n([\d\w]{2})\n(.+)\n([\d.]+)'
matches = re.findall(pattern, content, re.MULTILINE)

with open("roster.txt", "w") as roster_output:
    for match in matches:
        roster_output.write(", ".join(match))
