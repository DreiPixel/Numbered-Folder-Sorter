import os  
import sys
import shutil
import random
import time

def pathinput():
    print("Numbered Folder sorter. \n basically sorts a number of files into numbered files. \n example: folder 1 has 4240 files and you specify that every folder only needs 1000 files \n this script automatically creates new folders and sorts them. \n DISCLAIMER: i have no idea how to optimize this since this is my first python script. \n")    
    while True:
        user_input = input("folder that contains numbered folders: ")
        user_exceptions = input("Any folder i should ignore? (example: .sync, memes, etc : ")            
        if os.path.exists(user_input) == False:
            print("path not found: " + str(user_input))
        else:
            directory = os.listdir(user_input)            
            try:
                directory.remove(user_exceptions)
                directory.sort(key=lambda line: int(line.split()[0]))
                return(user_input, user_exceptions)
                break
            except ValueError as e: 
                print("folder contains folder with a string. please use only numbered folders \n or the exceptions folder doesnt exist." , e )              

user_input, user_exceptions = pathinput()

def filenumber():
    while True:
        try:
            user_files = int(input("how many files in a folder?: "))
            return(user_files)
            break
        except ValueError:
            print("not a number")
        
#user_input = pathinput()
user_files = filenumber()

def sortdirectorylist():    
    directory = os.listdir(user_input)
    directory.remove(user_exceptions)
    directory.sort(key=lambda line: int(line.split()[0]))    
    return directory

def listfiles(n):
    directorysorted = sortdirectorylist()
    d = len(os.listdir(user_input + ("\\") + directorysorted[n]))
    return d

def finalsort():
    i = 0
    directorysorted = sortdirectorylist()
    length = len(directorysorted)
    sorting = []
    sortinot = []
    while i < length:  
        #print("folder: " + str(i + 1) + " | files: " + str(listfiles(i)))
        if listfiles(i) > int(user_files):           
            sorting.append(i + 1)
        elif listfiles(i) < int(user_files):       
            sortinot.append(i + 1) 
        i  += 1
    return sorting, sortinot


    
sortthis, sortinto = finalsort()


while len(sortthis) != False: 
    directorysorted = sortdirectorylist()
    sortthis, sortinto = finalsort()
    try:
        files = os.listdir(user_input + ("\\") + str(sortthis[0]))
        file = random.choice(files)
        if len(sortinto) == False:
            lastdir = int(directorysorted[-1])
            makedir = lastdir + 1
            os.mkdir(os.path.join(user_input, str(makedir)))
        else:
            sortinto2 = os.path.join(user_input, str(sortinto[0]))
            shutil.move(os.path.join(user_input, str(sortthis[0]), file), sortinto2)
    except:
        break
print("Finished / Nothing to sort.")


