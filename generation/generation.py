#!/usr/bin/python3

import sys
import subprocess
import os
import struct
from random import randint
from shutil import copyfile

class Image:

    def __init__(self):
        #initialises default values
        self.version = 0
        self.authorName = 0
        self.width = 0
        self.height = 0
        self.numColours = 0
        self.colourTable = []
        self.pixels = []
        self.realWidth = 0
        self.realHeight = 0
        self.realNumColour = 0
        self.noAuthor = False

    def randomImageParameters(self):
        # one percent of the time the version will be between 20 and 29, otherwise it happpened too often.
        if randint(0, 1000) <= 10 :
            self.version = randint(20, 29)
        else:
            self.version = (list(range(0, 19)) + list(range(30, 101)))[randint(0, 89)]
        # the missing author is actually just a way to make the program crash by making the converter never find a 00 byte to finish the author name
        if randint(0, 1000) <= 10:
            self.noAuthor = True
            while True:
                self.width = randint(286331153, 4294967295)
                if "00" not in hex(self.width):
                    break
            while True:
                self.height = randint(286331153, 4294967295)
                if "00" not in hex(self.height):
                    break
            while True:
                self.numColours = randint(286331153, 4294967295)
                if "00" not in hex(self.numColours):
                    break
        else:
            # After quite a bit of testing, the fact that the height or the num of colours is higher than roughly 2100000000 often makes the converter crash
            self.authorName = randint(0, 16777215)
            self.width = randint(0, 100)
            a = randint(0, 2250000000)
            b = randint(0, 100)
            if randint(0, 10) >= 5:
                self.height = a
                self.numColours = b
            else:
                self.height = b
                self.numColours = a
        self.realHeight = randint(0, 200)
        self.realHeight = randint(0, 200)
        self.realNumColour = randint(0, 257)


    def setColourTable(self, c):
        self.colourTable = c


    def setPixels(self, p):
        self.pixels = p
    
    def savePicture(self, fileName):
        #make the file
        with open(fileName, 'w+b') as saveFile:
            #add the beggining thing
            saveFile.write((52651).to_bytes(2, 'little'))
            #print((52651).to_bytes(2, 'little'))
            #add the version   
            saveFile.write(self.version.to_bytes(2, 'little'))
            #add the author name
            if self.noAuthor == False:
                saveFile.write(self.authorName.to_bytes(3, 'little'))
            #    print(self.authorName.to_bytes(3, 'little'))
                saveFile.write((0).to_bytes(1, 'little'))
            #    print((0).to_bytes(1, 'little'))
            #add the width
            saveFile.write(self.width.to_bytes(4, 'little'))
            #print(self.width.to_bytes(4, 'little'))
            #add the height
            saveFile.write(self.height.to_bytes(4, 'little'))
            #print(self.height.to_bytes(4, 'little'))
            #add the numof colours
            saveFile.write(self.numColours.to_bytes(4, 'little'))
            #print(self.height.to_bytes(4, 'little'))
            #add the colour table
            for colour in self.colourTable:
                saveFile.write(colour.to_bytes(4, 'little'))
            #add the pixels
            for pixel in self.pixels:
                saveFile.write(pixel.to_bytes(1, 'little'))

    def pictureToString(self):
        return "v" + str(self.version) + "_a" + hex(self.authorName) + "_w" + str(self.width) + "_h" + str(self.height) + "_nc" + str(self.numColours) + "_na" +str(self.noAuthor)


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
        main.image.colourTable = chooseRandomColour(main.image.realNumColour)
        main.image.setPixels(getRandomPixels(main.image))
        main.image.savePicture(tempImageFileName)
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
        for w in range(image.realWidth):
            for h in range(image.realHeight):
                pixels += [randint(0, len(image.colourTable)-1)]
    #print(pixels)
    return pixels

def testImage(image, crashedFileName):
    # testing the file using the converter tool 
    pipes = subprocess.Popen(['../converter', image , 'outputImage'], stderr=subprocess.PIPE)
    std_err = pipes.communicate()
    # if the program crashes
    if pipes.returncode != 0 and std_err[1].decode("utf-8").find('crashed'):
        os.rename(image, "./fourFuzzer/" + crashedFileName + ".img")
        #main.image.saveHexPicture("./crashingTextFiles/" + crashedFileName + ".txt")
        main.outputFileNb += 1

if __name__ == "__main__":
    subprocess.Popen(['mkdir', 'fourFuzzer'])
    main()