#pyex3.py - read roster.txt fields into a dictionary
#Evan Gardner
#s1270495
#CS-371
#Spring 2023

input_file = open('roster.txt', 'r')

roster = {}
for student in input_file.readlines():
    [last, first, email] =student.split(',')

    email = email.rstrip()

    # Get id from email
    #[id, domain] = email.split('@')
    id = email.replace('@monmouth.edu', '')
    #insert student into roster dict with key = id
    roster[id] = last + ", " + first

#print roster
for id in sorted(roster.keys()):
    print(id + ', '+ roster[id])

