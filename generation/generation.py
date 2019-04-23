#!/usr/bin/python3

import sys
import subprocess
import os
import struct
from random import randint
from shutil import copyfile

TEST_VERSIONS = list(range(0, 102))
TEST_AUTHOR_NAMES = [ i*256 for i in range(4250, 4450) ] #the *256 is there just to add 00 at the end
TEST_WIDHTS = list(range(0, 200))
TEST_HEIGHTS = list(range(0, 200))
TEST_NUM_COLOURS = list(range(0, 257))

class Image:

    def __init__(self):
        self.version = 0
        self.authorName = 0
        self.width = 0
        self.height = 0
        self.numColours = 0
        self.colourTable = []
        self.pixels = []

    def randomImageParameters(self):
        self.version = TEST_VERSIONS[randint(0, len(TEST_VERSIONS))-1]
        self.authorName = TEST_AUTHOR_NAMES[randint(0, len(TEST_AUTHOR_NAMES))-1]
        self.width = TEST_WIDHTS[randint(0, len(TEST_WIDHTS))-1]
        self.height = TEST_HEIGHTS[randint(0, len(TEST_HEIGHTS))-1]
        self.numColours = TEST_NUM_COLOURS[randint(0, len(TEST_NUM_COLOURS))-1]

    def setColourTable(self, c):
        self.colourTable = c


    def setPixels(self, p):
        self.pixels = p
    
    def savePicture(self, fileName):
        #make the file
        with open(fileName, 'w+b') as saveFile:
            #add the beggining thing
            saveFile.write((52651).to_bytes(2, 'little'))
            #add the version   
            saveFile.write(self.version.to_bytes(2, 'little'))
            #add the author name
            saveFile.write(self.authorName.to_bytes(3, 'big'))
            #add the width
            saveFile.write(self.width.to_bytes(4, 'little'))
            #add the height
            saveFile.write(self.height.to_bytes(4, 'little'))
            #add the numof colours
            saveFile.write(self.numColours.to_bytes(4, 'little'))
            #add the colour table
            for colour in self.colourTable:
                saveFile.write(colour)
            #add the pixels
            for pixle in self.pixels:
                saveFile.write(pixel.to_bytes(2, 'little'))


def main():
    # if main is not well formated
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " [Number of Tests]")
        exit(1)
    numberOfTests = int(sys.argv[1])
    tempImageFileName = "temp.img"
    main.outputFileNb = 0
    main.kindOfError = {'width':[], 'height':[], 'version':[], 'zeroColour':[], 'tooManyColours':[], 'authorContains00':[]}
    for x in range(numberOfTests):
        print("Test nÂ°",str(x),sep='',end="\r",flush=True)
        main.image = Image()
        main.image.randomImageParameters()
        main.image.colourTable = chooseRandomColour(main.image.numColours)
        main.image.pixles = getRandomPixels(main.image)
        #This is done to indicate which files to look at, once files that do not work have been found
        handleKnownErrors()
        main.image.savePicture(tempImageFileName)
        testImage(tempImageFileName)
    try:
        os.remove(tempImageFileName) #if last file failed this file will not exist
    except:
        pass
    print(main.kindOfError)
      
def handleKnownErrors():
    if main.image.width == 0 :
        main.kindOfError['width'] += [main.outputFileNb]
    elif main.image.height == 0 :
        main.kindOfError['height'] += [main.outputFileNb]
    elif main.image.version > 100 :
        main.kindOfError['version'] += [main.outputFileNb]
    elif main.image.numColours <= 0 :
        main.kindOfError['zeroColour'] += [main.outputFileNb]
    elif main.image.numColours > 255 :
        main.kindOfError['tooManyColours'] += [main.outputFileNb]
    elif main.image.authorName == 4352*256 :
        main.kindOfError['authorContains00'] += [main.outputFileNb]

def chooseRandomColour(numOfColour):
    allColours = []
    if (numOfColour not in [-1, 0]):
        for n in range(numOfColour):
            allColours += [randint(0, 2147483647).to_bytes(4, 'little')]
    return allColours

def getRandomPixels(image):
    pixels = []
    if (len(image.colourTable) > 0):
        if (image.width not in [-1, 0]) and (image.height not in [-1, 0]):
            for w in range(image.width):
                line = []
                for h in range(image.height):
                    line += [randint(0, len(image.colourTable)-1)]
                pixels += [line]
    return pixels

def testImage(image):
    pipes = subprocess.Popen(['../converter', image , 'outputImage'], stderr=subprocess.PIPE)
    std_err = pipes.communicate()
    
    if pipes.returncode != 0 and std_err[1].decode("utf-8").find('crashed'):
        os.rename(image, "./crashingImages/testinput" + str(main.outputFileNb) + ".img")
        main.outputFileNb += 1
        

if __name__ == "__main__":
    main()