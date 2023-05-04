#pyex2.py - word length occurrences in english sorted
#Evan Gardner
#s1270495
#CS-371
#Spring 2023

#create input file object
input_file = open('english.sorted', 'r')

#declare empty dictionary
wordlengths = {}

#iterate through lines of input_file
for word in input_file.readlines():#readlines() creates a list
    length = len(word) -1 # subtract 1for hidden \n char in word

    if(length in wordlengths): #if key=length already in wordlengths
        wordlengths[length] += 1 # increment value in wordlengths where key= length
    else:                       # length is a brand new key
        wordlengths[length] = 1 # initialize new value at new key = length

#print word length occurrences table 
print("word length\t\tOccurrences")

for length in sorted(wordlengths.keys()):
    # print(str(length)  + '\t\t\t' + str(wordlengths[length]))
    #print("%i\t\t\t%i" % (length, wordlengths[length]))
    print(f'{length}\t\t\t{wordlengths[length]}')