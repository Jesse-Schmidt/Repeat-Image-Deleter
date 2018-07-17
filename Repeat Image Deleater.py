import os
from PIL import Image
import random
import time

def Generate_Image_Hash(photo):
    current = Image.open(photo)
    current = current.resize((8, 8), Image.ANTIALIAS)
    current = current.convert("L")
    (w, h) = current.size
    mean = sum(list(current.getdata()))/64
    bits = ""
    for height in range(h):
        for width in range(w):
            color = current.getpixel((width, height))
            if color < mean:
                bits += "0"
            else:
                bits += "1"
    hash = str(int(bits, 2).__format__("016x").upper())
    current.close()
    return hash

def Hammer_Distance(hash1, hash2):
    assert len(hash1) == len(hash2)
    difference = 0
    for count in range(len(hash1)):
        if hash1[count] != hash2[count]:
            difference += 1
    return difference

class LinkedList:
    def __init__(self, duplicates = None,  next=None):
        self.duplicates = []
        self.next = None

    def getNames(self):
        return self.duplicates

    def getNext(self):
        return self.next

    def setNext (self, newest):
        self.next = newest

    def addData(self, fileName):
        self.duplicates.append(fileName)

def getHashes(files_found):
    file_hash = {}
    hash_file = {}
    for file in files_found:
        hash = Generate_Image_Hash(file)
        file_hash[file] = hash
        hash_file[hash] = file
    return [file_hash, hash_file]


def BruteForceMethod(files_found):
    duplicates = []
    resources = getHashes(files_found)
    file_hash = resources[0]
    hash_file = resources[1]
    for x in range(len(file_hash) - 1):
        for y in range(x + 1, len(file_hash)):
            difference = Hammer_Distance(file_hash[files_found[x]], file_hash[files_found[y]])
            if difference < 5:
                duplicates.append(files_found[x])
                break

    for file in duplicates:
        file_name = file.split("\\")
        file_name = file_name[len(file_name) - 1]
        if not os.path.exists(parent_dir + "\\Duplicates"):
            os.makedirs(parent_dir + "\\Duplicates")
        try:
            os.rename(file, (parent_dir + "\\Duplicates\\" + file_name))
        except:
            os.rename(file, (parent_dir + "\\Duplicates\\" + str(random.randint(0, 100)) + file_name))
    return len(duplicates)

def LinkedListMethod(files_found):
    resources = getHashes(files_found)
    duplicatesList = None
    file_hash = resources[0]
    hash_file = resources[1]
    for x in range(len(file_hash)):
        bestEntry = None
        bestHammer = 5
        if duplicatesList is None:
                duplicatesList = LinkedList()
                duplicatesList.addData(files_found[x])

        else:
            current = duplicatesList
            found = False
            while current is not None:
                tests = current.getNames()
                difference = Hammer_Distance(file_hash[files_found[x]], file_hash[tests[0]])
                if difference < 2:
                    if difference < bestHammer:
                        bestHammer = difference
                        bestEntry = current

                current = current.getNext()
            if bestEntry is None:
                head = LinkedList()
                head.addData(files_found[x])
                head.setNext(duplicatesList)
                duplicatesList = head
            else:
                bestEntry.addData(files_found[x])

    current = duplicatesList
    count = 1
    duplicates = 0
    while current is not None:
        names = current.getNames()
        duplicateFolder = parent_dir + "\\Duplicates"
        if not os.path.exists(duplicateFolder):
            os.makedirs(duplicateFolder)
        if len(names) > 1:
            newDuplicatesFolder = duplicateFolder + "\\" + str(count)
            if not os.path.exists(newDuplicatesFolder):
                os.makedirs(newDuplicatesFolder)
            count += 1
            for file in names:
                file_name = file.split("\\")
                file_name = file_name[len(file_name) - 1]
                duplicates += 1
                try:
                    os.rename(file, (newDuplicatesFolder + "\\" + file_name))
                except:
                    os.rename(file, (newDuplicatesFolder + "\\" + str(random.randint(0, 100)) + file_name))
        current = current.getNext()
    return duplicates

start_time = time.time()
files_found = []

parent_dir = input("Please enter the parent directory that you want to process\n")

#finds all the images in the parent directory
for root, dirs, files in os.walk(parent_dir, topdown=False):
    for name in files:
        if name[len(name) - 4 : len(name)].lower() == ".jpg" or name[len(name) - 4 : len(name)].lower() == ".png":
            files_found.append(os.path.join(root, name))

duplicates = LinkedListMethod(files_found)
end_time = time.time()

print("Searched files: " + str(len(files_found)))
print("Duplicates found: " + str(duplicates))
print("Total time taken: " + str(end_time - start_time) + " seconds")