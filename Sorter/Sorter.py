import os
import sys
import shutil
import random
import zlib

print("Numbered Folder sorter. \nbasically sorts a number of files into numbered files. \nexample: folder 1 has 4240 files and you specify that every folder only needs 1000 files \nthis script automatically creates new folders and sorts them. \nif a folder is inside a numbered folder it treats it as a file so it gets sorted. \nit ignores any folder that is not numbered in the main folder.\nDISCLAIMER: i have no idea how to optimize this since this is my first python script. \n")

#This ask the user for a Valid path.
while True:
    user_input = input("folder that contains numbered folders: \n ")
    if os.path.exists(user_input) == False:
        print("path not found: " + str(user_input) + "\n ")
    else:
        directory = os.listdir(user_input)
        break


#This ask the user for a Valid number of files
while True:
    try:
        file_amount = int(input("how many files in a folder?: \n "))
        break
    except ValueError:
        print("not a number \n")

#This sorts the Folders so thats it is not 1 10 11
directorysorted = []
for item in directory:
    for subitem in item.split():
        if(subitem.isnumeric()):
            directorysorted.append(subitem)
directorysorted.sort(key=lambda line: int(line.split()[0]))

#This ask the user for any folder number that is should ignore and removes it from the list.
user_exceptions = input("Any folders i should ignore? separate with space (example: 1 2 5 7) :\n ")
if len(user_exceptions) == True:
    userList = user_exceptions.split(" ")
    directorysorted = [x for x in directorysorted if x not in userList]


#we are gonna check the CRC of a fi if it already exist in a folder
def crc32(fileName):
    with open(fileName, 'rb') as fh:
        hash = 0
        while True:
            s = fh.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)

#this ask the user for a source folder and moves them into the folder 1. if it doesn't exists it will create it in the user input directory
user_source = input("Any input folder? (if a folder is here it will take all files and puts them into the folder 1): \n ")
if os.path.exists(user_source) == True:
    filessource = os.listdir(user_source)
    while True:
        if os.path.exists(os.path.join(user_input, str(1))) == True:
            directorysorted.insert(0, 1)
            for f in filessource:
                try:
                    shutil.move(os.path.join(user_source, f), os.path.join(user_input, str(directorysorted[0])))
                except:
                    checksum = crc32(os.path.join(user_source, f))
                    filename, fileext = os.path.splitext(f)
                    print(" File " + f + " already existed in " + os.path.join(user_input, str(directorysorted[0])) + "\n", " replaced filename with " + filename + " - " + checksum + fileext)
                    shutil.move(os.path.join(user_source, f), os.path.join(user_input, str(directorysorted[0]), filename + " - " + checksum + fileext))
            break
        else:
            os.mkdir(os.path.join(user_input, str(1)))


#this just checks the amount of files in a folder and returns the amount
def listfiles(n):
    d = len(os.listdir(user_input + ("\\") + str(directorysorted[n])))
    return d




# This decides what folder to take from and what folder to sort into and what folders to delete (when they are empty)
def finalsort():
    i = 0
    amount = len(directorysorted)
    sorting = []
    sortinto = []
    empty = []
    while i < amount:
        if listfiles(i) > int(file_amount):
            sorting.append(directorysorted[i])
        if listfiles(i) < int(file_amount):
            sortinto.append(directorysorted[i])
        if listfiles(i) == 0:
            empty.append(directorysorted[i])
        i  += 1
    return sorting, sortinto, empty



#this deletes empty folders
sortthis, sortinto, empty = finalsort()
while len(empty) != False:
    shutil.rmtree(os.path.join(user_input, str(empty[0])))
    directorysorted.remove(empty[0])
    empty.pop(0)

#this fils empty space of folder so we dont have 13 16 17
for i in range(len(directorysorted)):
    foldercheck = i + 1
    if foldercheck != int(directorysorted[i]):
        os.mkdir(os.path.join(user_input, str(foldercheck)))
        directorysorted.insert(i, str(foldercheck))

#sorts folders that are lower than the designated number so that every folder exact number of the wanted files in a folder
sortthis, sortinto, empty = finalsort()
while len(sortinto) > 1:
    sortthis, sortinto, empty = finalsort()
    if listfiles(int(sortinto[-1]) - 1) == 0:
        shutil.rmtree(os.path.join(user_input, str(sortinto[-1])))
        directorysorted.pop(int(sortinto[-1]) - 1)
        sortinto.pop(-1)
    if len(sortinto) == 1:
        break
    sortthis, sortinto, empty = finalsort()
    files = os.listdir(user_input + ("\\") + str(sortinto[-1]))
    file = random.choice(files)
    if listfiles(-1) != 0:
        try:
            shutil.move(os.path.join(user_input, str(sortinto[-1]), file), os.path.join(user_input, str(sortinto[0])))
        except:
            checksum = crc32(os.path.join(user_input, str(sortinto[-1]), file))
            filename, fileext = os.path.splitext(file)
            print(" File " + file + " already existed in " + os.path.join(user_input, str(sortinto[0])) + "\n" + " replaced filename with " + filename + " - " + checksum + fileext)
            shutil.move(os.path.join(user_input, str(sortinto[-1]), file), os.path.join(user_input, str(sortinto[0]), filename + " - " + checksum + fileext))



#this is the final execution and decides what file to move per random and puts it into the first "empty" folder until it hits the designated number
while len(sortthis) != False:
    sortthis, sortinto, empty = finalsort()
    try:
        files = os.listdir(user_input + ("\\") + str(sortthis[0]))
        file = random.choice(files)
        if len(sortinto) == False:
            lastdir = int(directorysorted[-1])
            makedir = lastdir + 1
            directorysorted.append(makedir)
            os.mkdir(os.path.join(user_input, str(makedir)))
        else:
            try:
                sortinto2 = os.path.join(user_input, str(sortinto[0]))
                shutil.move(os.path.join(user_input, str(sortthis[0]), file), sortinto2)
            except:
                checksum = crc32(os.path.join(user_input, str(sortthis[0]), file))
                filename, fileext = os.path.splitext(file)
                print(" File " + file + " already existed in " + os.path.join(user_input, str(sortinto[0])) + "\n" + " replaced filename with " + filename + " - " + checksum + fileext)
                shutil.move(os.path.join(user_input, str(sortthis[0]), file), os.path.join(sortinto2, filename + " - " + checksum + fileext))
    except:
        break

print("\n Finished / Nothing to sort.")



