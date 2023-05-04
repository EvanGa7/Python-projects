#pyex4.py - Read multiline records fille and write it as a single line record
#Evan Gardner
#s1270495
#CS-371
#Spring 2023

import re

#
input_roster = open('cs176roster.webadvisor.txt', 'r').read()

student_pattern = re.compile('.+, .+\n[0-9]{7}')


students = student_pattern.findall(input_roster)

print(students)


for student in students:
    student = student.replace('\n',  ', s')
    print(student)

outfile = open('rpster2.txt', 'w')
for student in students:
    student = student.replace('\n', ', s')
    outfile.write(student + '\n')

outfile.close()

