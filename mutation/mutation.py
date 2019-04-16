#!/usr/bin/python3

import sys
import subprocess
import os
import struct
from random import randint
from shutil import copyfile

def main():
    if (len(sys.argv) != 5):
        print("Usage: " + sys.argv[0] + " [inputFile] [nbOfTestRuns] [nbOfModifications] [percentageOfBytesToModify]")
        exit(1)

    correctImage = sys.argv[1]
    nbTestRuns = int(sys.argv[2])
    maxModififications = int(sys.argv[3])
    percentageModification = float(sys.argv[4])
    
    main.nbOfBytesModified = 0
    main.nbOfBytesToModify = round(os.path.getsize(correctImage) * percentageModification)
    print("nb of bytes to modify " + str(main.nbOfBytesToModify))

    main.hasCrashed = False
    main.nbOfColors = 0
    main.nameLength = 0
    main.outputFileNb = 0

    with open(correctImage, 'rb') as file:
        file.seek(18)
        main.nbOfColors = struct.unpack("<hh", file.read(4))[0]

        file.seek(4)
        while True:
            if (ord(file.read(1)) == 0): break
            main.nameLength += 1

    print("Started fuzzing ! \nAll crashing input files will be put in the folder 'crashingImages'.")

    for x in range(nbTestRuns):
        print ("Test run n°" + str(x) + " ...")

        for y in range(maxModififications):
            infoToTest = randint(0, 6)
            
            try:
                if (infoToTest == 0):
                    if(testVersion(correctImage)): break
                elif (infoToTest == 1):
                    if(testAuthor(correctImage)): break
                elif (infoToTest == 2):
                    if(testDimension(correctImage, 5 + main.nameLength)): break
                elif (infoToTest == 3):
                    if(testDimension(correctImage, 9 + main.nameLength)): break
                elif (infoToTest == 4):
                    if(testColorTable(correctImage)): break
                elif (infoToTest == 5):
                    if(testNumColors(correctImage)): break
                else:
                    if(testPixels(correctImage)): break

                testImage(correctImage)
            except FileNotFoundError:
                print("The file '" + correctImage + "' does not exists.")
                exit(1)

        if (main.nbOfBytesToModify >= main.nbOfBytesModified): print("Max number of modifications reached, ending test run.")
        main.nbOfBytesModified = 0
        main.hasCrashed = False

def testVersion(correctImage):
    with open(correctImage, 'r+b') as file:
        file.seek(2, 1)
        newVersion = randint(0, 255).to_bytes(2, 'little')
        file.write(newVersion)

        main.nbOfBytesModified += 2
        if (main.nbOfBytesToModify >= main.nbOfBytesModified): return True
    
    return False

def testAuthor(correctImage):
    with open("tmpFile", "w+b") as newFile, open(correctImage, 'r+b') as oldFile:
        newFile.write(oldFile.read(4))
        nameLength = randint(0, 255)

        for x in range(0, nameLength):
            newFile.write(randint(0, 128).to_bytes(1, 'little'))
            main.nbOfBytesModified += 1
            if (main.nbOfBytesToModify >= main.nbOfBytesModified): return True
        
        newFile.write(int(0).to_bytes(1, 'little'))
        
        oldFile.seek(4 + main.nameLength)
        newFile.write(oldFile.read())
        
        main.nameLength = nameLength

    os.remove(correctImage)
    os.rename("tmpFile", correctImage)
    
    return False

def testDimension(correctImage, index):
    with open(correctImage, 'r+b') as file:
        file.seek(index, 1)
        file.write(randint(0, 2147483647).to_bytes(4, 'little'))
        
        main.nbOfBytesModified += 4
        if (main.nbOfBytesToModify >= main.nbOfBytesModified): return True
    
    return False

def testNumColors(correctImage):
    with open(correctImage, 'r+b') as file:
        file.seek(13 + main.nameLength, 1)
        file.write(randint(0, 255).to_bytes(4, 'little'))
        
        main.nbOfBytesModified += 4
        if (main.nbOfBytesToModify >= main.nbOfBytesModified): return True
    
    return False

def testColorTable(correctImage):
    with open("tmpFile", 'w+b') as newFile, open(correctImage, "r+b") as oldFile:
        newFile.write(oldFile.read(17 + main.nameLength))# data is written to the new file until the first color

        nbColors = randint(0, 255)
        
        for x in range(nbColors):
            newFile.write(randint(0, 2147483647).to_bytes(4, 'little'))# write new random colors
            main.nbOfBytesModified += 4
            if (main.nbOfBytesToModify >= main.nbOfBytesModified): return True

        oldFile.seek(oldFile.tell() + (main.nbOfColors * 4))# move the pointer to the address of the first pixel and forget about old colors
        newFile.write(oldFile.read())
        main.nbOfColors = nbColors
    
    os.remove(correctImage)
    os.rename("tmpFile", correctImage)

    return False

def testPixels(correctImage):
    with open(correctImage, 'r+b') as file:
        nbOfColors = randint(0, 255)
        file.seek(21 + (main.nbOfColors * 4))
        file.truncate()

        for x in range(nbOfColors):
            color = randint(0, 128).to_bytes(1, 'little')
            file.write(color)
            
            main.nbOfBytesModified += 1
            if (main.nbOfBytesToModify >= main.nbOfBytesModified): return True
    
    return False

def testImage(image):
    pipes = subprocess.Popen(['../converter', image, 'outputImage'], stderr=subprocess.PIPE)
    std_err = pipes.communicate()

    if (pipes.returncode != 0 and std_err[1].decode("utf-8").find('crashed')):
        print("Found a bug !")
        os.rename(image, "crashingImages/testinput" + str(main.outputFileNb) + ".img")
        main.outputFileNb += 1
        main.hasCrashed = True
        copyfile("../testinput.img", "testinput.img")

if __name__ == "__main__":
    main()