#pyex1.py-standard input in Python
#Evan Gardner
#s1270495
#CS-371
#Spring 2023

import sys

for line in sys.stdin:
    #sys.stdout.write(line)
    print(len(line))
    print(len(line.rstrip()))
