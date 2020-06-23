import os
import sys
import shutil
import random


print(" Numbered Folder sorter. \n basically sorts a number of files into numbered files. \n example: folder 1 has 4240 files and you specify that every folder only needs 1000 files \n this script automatically creates new folders and sorts them. \n if a folder is inside a numbered folder it treats it as a file so it gets sorted. \n it ignores any folder that is not numbered in the main folder.\n DISCLAIMER: i have no idea how to optimize this since this is my first python script. \n")

#This ask the user for a Valid path.
while True:
    user_input = input(" folder that contains numbered folders: \n")
    if os.path.exists(user_input) == False:
        print("path not found: " + str(user_input))
    else:
        directory = os.listdir(user_input)
        break


#This ask the user for a Valid number of files
while True:
    try:
        file_amount = int(input(" how many files in a folder?: \n"))
        break
    except ValueError:
        print(" not a number")

#This sorts the Folders so thats it is not 1 10 11
directorystr = os.listdir(user_input)
directorysorted = []
for item in directorystr:
    for subitem in item.split():
        if(subitem.isnumeric()):
            directorysorted.append(subitem)
directorysorted.sort(key=lambda line: int(line.split()[0]))

#This ask the user for any folder number that is should ignore and removes it from the list.
user_exceptions = input(" Any folders i should ignore? separate with space (example: 1 2 5 7) :\n")
if len(user_exceptions) == True:
    userList = user_exceptions.split(" ")
    directorysorted = [x for x in directorysorted if x not in userList]


#this ask the user for a source folder and moves them into the folder 1. if it doesn't exists it will create it in the user input directory
user_source = input(" Any input folder? (if a folder is here it will take all files and puts them into the folder 1): \n")
if os.path.exists(user_source) == True:
    filessource = os.listdir(user_source)
    while True:
        if os.path.exists(os.path.join(user_input, str(1))) == True:
            directorysorted.insert(0, 1)
            for f in filessource:
                shutil.move(os.path.join(user_source, f), os.path.join(user_input, str(directorysorted[0])))
            break
        else:
            os.mkdir(os.path.join(user_input, str(1)))


#this just checks the amount of files in a folder and returns the amount
def listfiles(n):
    d = len(os.listdir(user_input + ("\\") + str(directorysorted[n])))
    return d


# This decides what folder to take from and what folder to sort into
def finalsort():
    i = 0
    length = len(directorysorted)
    sorting = []
    sortinot = []
    while i < length:
        if listfiles(i) > int(file_amount):
            sorting.append(directorysorted[i])
        elif listfiles(i) < int(file_amount):
            sortinot.append(directorysorted[i])
        i  += 1
    return sorting, sortinot

#this is the final execution and decides what file to move per random and puts it into the first "empty" folder until it hits the designated number
sortthis, sortinto = finalsort()
while len(sortthis) != False:
    sortthis, sortinto = finalsort()
    try:
        files = os.listdir(user_input + ("\\") + str(sortthis[0]))
        file = random.choice(files)
        if len(sortinto) == False:
            lastdir = int(directorysorted[-1])
            makedir = lastdir + 1
            directorysorted.append(makedir)
            os.mkdir(os.path.join(user_input, str(makedir)))
        else:
            sortinto2 = os.path.join(user_input, str(sortinto[0]))
            shutil.move(os.path.join(user_input, str(sortthis[0]), file), sortinto2)
    except:
        break

print(" Finished / Nothing to sort.")


