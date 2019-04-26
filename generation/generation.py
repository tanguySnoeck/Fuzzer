#!/usr/bin/python3

import sys
import subprocess
import os
import struct
from random import randint
from shutil import copyfile

#These values can be changed if needed to make the explored space smaller or larger.
TEST_VERSIONS = list(range(0, 102)) #number higher than 100 do not make the program crash, it just exits in a predictable way
TEST_AUTHOR_NAMES = [ i*256 for i in range(4300, 4400) ] #the *256 is there just to add 00 at the end
TEST_WIDHTS = list(range(0, 200))
TEST_HEIGHTS = list(range(0, 200))
TEST_NUM_COLOURS = list(range(0, 257))
#TODO add the likelyhood of another colour added
#TODO add likelyhood of a missing pixel or one too much

class Image:

    def __init__(self):
        #initialises default values
        self.version = 0
        self.authorName = 0
        self.width = 0
        self.height = 0
        self.numColours = 0
        self.realNumColour = True
        self.colourTable = []
        self.pixels = []
        self.realNumPixel = True

    def randomImageParameters(self):
        self.version = TEST_VERSIONS[randint(0, len(TEST_VERSIONS))-1]
        self.authorName = TEST_AUTHOR_NAMES[randint(0, len(TEST_AUTHOR_NAMES))-1]
        self.width = TEST_WIDHTS[randint(0, len(TEST_WIDHTS))-1]
        self.height = TEST_HEIGHTS[randint(0, len(TEST_HEIGHTS))-1]
        self.numColours = TEST_NUM_COLOURS[randint(0, len(TEST_NUM_COLOURS))-1]
        if randint(0, 100) == 50 and self.numColours > 1:
            self.realNumColour = False
        if randint(0, 100) == 1 and (self.width > 1 and self.height > 1):
            self.realNumPixel = False

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
            saveFile.write(self.authorName.to_bytes(3, 'little'))
            saveFile.write((0).to_bytes(1, 'little'))
            #add the width
            saveFile.write(self.width.to_bytes(4, 'little'))
            #add the height
            saveFile.write(self.height.to_bytes(4, 'little'))
            #add the numof colours
            #if self.realNumColour:
            saveFile.write(self.numColours.to_bytes(2, 'little'))
            #else:
            #    saveFile.write((self.numColours - 1).to_bytes(4, 'little'))
            #add the colour table
            for colour in self.colourTable:
                saveFile.write(colour.to_bytes(4, 'little'))
            #add the pixels
            #if self.realNumPixel:
            for pixel in self.pixels:
                saveFile.write(pixel.to_bytes(2, 'little'))
            #else:
            #    for pixel in self.pixels[0:len(self.pixels)-1]:
            #        saveFile.write(pixel.to_bytes(2, 'little'))

    def saveHexPicture(self, fileName):
        with open(fileName, 'w') as saveFile:
            saveFile.write("ab cd\n")
            #add the version   
            saveFile.write(hex(self.version)[2:]+"\n")
            #add the author name
            saveFile.write(hex(self.authorName)[2:] + "00" +"\n")
            #add the width
            saveFile.write(hex(self.width)[2:]+"\n")
            #add the height
            saveFile.write(hex(self.height)[2:]+"\n")
            #add the numof colours
            #if self.realNumColour:
            saveFile.write(hex(self.numColours)[2:]+"\n")
            #else:
            #    saveFile.write((self.numColours - 1).to_bytes(4, 'little'))
            #add the colour table
            for colour in self.colourTable:
                saveFile.write(hex(colour)[2:]+"\n")
            #add the pixels
            #if self.realNumPixel:
            for h in range(self.height-1):
                for p in [hex(pixel) for pixel in self.pixels[h*self.width:h*(self.width)+self.width]]:
                    saveFile.write(p[2:] + " " )
                saveFile.write("\n")


    def pictureToString(self):
        return "v" + str(self.version) + "_a" + hex(self.authorName) + "_w" + str(self.width) + "_h" + str(self.height) + "_nc" + str(self.numColours) + "_rnc" + str(self.realNumColour) + "_rnp" + str(self.realNumPixel)


def main():
    # if main is not well formated
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " [Number of Tests]")
        exit(1)
    numberOfTests = int(sys.argv[1])
    tempImageFileName = "temp.img"
    main.outputFileNb = 0
    for x in range(numberOfTests):
        print("Test n°",str(x),sep='',end="\r",flush=True)
        #creating a random image
        main.image = Image()
        main.image.randomImageParameters()
        main.image.colourTable = chooseRandomColour(100)
        main.image.setPixels(getRandomPixels(main.image))
        #print(main.image.pixels)
        main.image.savePicture(tempImageFileName)
        #main.image.savePicture(main.image.pictureToString())
        testImage(tempImageFileName, main.image.pictureToString())
    try:
        os.remove(tempImageFileName) #if last file failed this file will not exist
    except:
        pass
    print("\n"+"number of crashed images: " + str(main.outputFileNb))

def chooseRandomColour(numOfColour):
    #This function creates a list of colours
    allColours = []
    if (numOfColour not in [-1, 0]):
        for n in range(numOfColour):
            allColours += [randint(0, 2147483647)]
    return allColours

def getRandomPixels(image):
    #This function creates a list of pixels (int)
    pixels = []
    if (len(image.colourTable) > 0):
        if (image.width not in [-1, 0]) and (image.height not in [-1, 0]):
            for w in range(image.width):
                for h in range(image.height):
                    pixels += [randint(0, len(image.colourTable)-1)]
    #print(pixels)
    return pixels

def testImage(image, crashedFileName):
    # testing the file using the converter tool 
    pipes = subprocess.Popen(['../converter', image , 'outputImage'], stderr=subprocess.PIPE)
    std_err = pipes.communicate()
    # if the program crashes
    if pipes.returncode != 0 and std_err[1].decode("utf-8").find('crashed'):
        os.rename(image, "./crashingImages/" + crashedFileName + ".img")
        main.image.saveHexPicture("./crashingTextFiles/" + crashedFileName + ".txt")
        main.outputFileNb += 1

if __name__ == "__main__":
    main()