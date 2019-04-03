#!/usr/bin/python3

import sys
import subprocess
import os
from random import randint
from shutil import copyfile

def main():
    if (len(sys.argv) != 5):
        print("Usage: " + sys.argv[0] + " myCorrectInputFile.img 200 100 0.01")
        return

    correctImage = sys.argv[1]
    nbTestRuns = int(sys.argv[2])
    maxModififications = int(sys.argv[3])
    percentageModification = sys.argv[4]
    
    outputFileNb = 0
    percentageChanged = 0

    main.hasCrashed = False

    for x in range(0, nbTestRuns):
        for y in range(0, maxModififications):
            # if (percentageChanged == percentageModification):
            #     break
            
            if (main.hasCrashed):
                break

            infoToTest = randint(0, 7)

            if (infoToTest == 0):
                testVersion(correctImage)
            elif (infoToTest == 1):
                testAuthor(correctImage)
            elif (infoToTest == 2):
                testWidth(correctImage)
            elif (infoToTest == 3):
                testHeight(correctImage)
            elif (infoToTest == 4):
                testColorTable(correctImage)
            elif (infoToTest == 5):
                testFirstColor(correctImage)
            elif (infoToTest == 6):
                testSecondColor(correctImage)
            else:
                testPixels(correctImage)

        main.hasCrashed = False
        copyfile("../testinput.img", "testinput.img")

def testVersion(correctImage):
    with open(correctImage, 'r+b') as file:
        file.seek(2, 1)
        newVersion = bytes([randint(0, 100)])
        file.write(newVersion)
    testImage()

def testAuthor(correctImage):
    return 
def testWidth(correctImage):
    return
def testHeight(correctImage):
    return
def testColorTable(correctImage):
    return
def testFirstColor(correctImage):
    return
def testSecondColor(correctImage):
    return
def testPixels(correctImage):
    return

def testImage():
    try:
        output = subprocess.check_output(['../converter', 'testinput.img', 'outputImage'], stderr=subprocess.STDOUT).decode("utf-8")
        print(output)

        if (output == "*** The program has crashed."):
            main.hasCrashed = True

        if (output != "*** The program has crashed." and os.path.isfile("outputImage")):
            os.remove("outputImage")
    except subprocess.CalledProcessError:
        pass
    
if __name__ == "__main__":
    main()