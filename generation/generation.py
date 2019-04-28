#!/usr/bin/python3

import sys
import subprocess
import os
import struct
from random import randint
from shutil import copyfile

CRASHING_IMAGES_FOLDER = "generationCrash"

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
        self.realWidth = 0      # to test what happens when the width declared is the the width used
        self.realHeight = 0     # to test what happens when the height declared is the the height used
        self.realNumColour = 0  # to test what happens when the number of colours declared is the the number of colours used
        self.noAuthor = False   # to trigger a crash.


    def randomImageParameters(self):
        # one percent of the time the version will be between 20 and 29, otherwise it happpened too often.
        if randint(0, 1000) <= 10 :
            self.version = randint(20, 29)
        else:
            self.version = (list(range(0, 19)) + list(range(30, 101)))[randint(0, 89)]

        # the missing author is actually just a way to make the program crash by making the converter never find a 00 byte to finish the author name
        if randint(0, 1000) <= 10:
            self.noAuthor = True

            # Making sure there are no 00 bytes in the following few arguments to ensure that the length of the author is way too long.
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
            # After quite a bit of testing, the fact that the height or the num of colours is higher than roughly 2100000000 often makes the converter crash (interpreted as negative values)
            self.authorName = randint(0, 16777215)
            self.width = randint(0, 100)
            # this was done to make sure that there would be images crashing only because of one non-valid argument at a time.
            a = randint(0, 2200000000)
            b = randint(0, 100)

            if randint(0, 10) >= 5:
                self.height = a
                self.numColours = b
            else:
                self.height = b
                self.numColours = a

        # these arguments will be used to generate the colour table and the pixel values.
        self.realHeight = randint(0, 200)
        self.realHeight = randint(0, 200)
        self.realNumColour = randint(0, 257)


    def setColourTable(self, c):
        #simple setter
        self.colourTable = c


    def setPixels(self, p):
        #simple setter
        self.pixels = p

    
    def savePicture(self, fileName):
        # Saves the image as a file
        with open(fileName, 'w+b') as saveFile:
            # Writes ab cd and version number
            saveFile.write((52651).to_bytes(2, 'little'))    # hex(52651) in little endian saves ab cd
            saveFile.write(self.version.to_bytes(2, 'little'))

            # If needed, writes the author name correctly
            if self.noAuthor == False:
                saveFile.write(self.authorName.to_bytes(3, 'little'))
                saveFile.write((0).to_bytes(1, 'little'))               # adding the 00 at the end of the author's name

            # Writes the width, height and numColour 
            saveFile.write(self.width.to_bytes(4, 'little'))
            saveFile.write(self.height.to_bytes(4, 'little'))
            saveFile.write(self.numColours.to_bytes(4, 'little'))

            #saves the colours and the pixels one by one
            for colour in self.colourTable:
                saveFile.write(colour.to_bytes(4, 'little'))
            for pixel in self.pixels:
                saveFile.write(pixel.to_bytes(1, 'little'))


    def pictureToString(self):
        # This function is used mainly to give good names to the saved files, so that the user can look through them to find a specific value / parameter.
        return "v" + str(self.version) + "_a" + hex(self.authorName) + "_w" + str(self.width) + "_h" + str(self.height) + "_nc" + str(self.numColours) + "_na" +str(self.noAuthor)


def main():
    # if main is not well formated
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " [Number of Tests]")
        exit(1)

    # initialising the main function
    numberOfTests = int(sys.argv[1])
    tempImageFileName = "temp.img"
    main.outputFileNb = 0

    print("Started fuzzing ! \nAll crashing input files will be put in the folder '" + CRASHING_IMAGES_FOLDER + "'.")
    for x in range(numberOfTests):
        print("Test n°",str(x),sep='',end="\r",flush=True)
        #creating a random image
        main.image = Image()
        main.image.randomImageParameters()
        main.image.colourTable = chooseRandomColour(main.image.realNumColour)
        main.image.setPixels(getRandomPixels(main.image))

        #saving the image as a temp file to test it
        main.image.savePicture(tempImageFileName)

        #testing the converter with this image
        testImage(tempImageFileName, main.image.pictureToString())

    # tries to remove the temp file if not already moved by testImage()
    try:
        os.remove(tempImageFileName) #if last file failed this file will not exist
    except:
        pass

    print("\n"+"number of crashed images: " + str(main.outputFileNb))


def chooseRandomColour(numOfColour):
    #This function creates a list of colours
    allColours = []
    if (numOfColour >= 0):
        for n in range(numOfColour):
            allColours += [randint(0, 2500000000)]
    return allColours


def getRandomPixels(image):
    #This function creates a list of pixels (int)
    pixels = []
    if (len(image.colourTable) > 0):
        for w in range(image.realWidth):
            for h in range(image.realHeight):
                pixels += [randint(0, len(image.colourTable)-1)]
    return pixels


def testImage(image, crashedFileName):
    # testing the file using the converter tool 
    pipes = subprocess.Popen(['../converter', image , 'outputImage'], stderr=subprocess.PIPE)
    #pipes = subprocess.Popen(['../converter_static', image, 'outputImage'], stderr=subprocess.PIPE)
    std_err = pipes.communicate()

    # if the program crashes
    if pipes.returncode != 0 and std_err[1].decode("utf-8").find('crashed'):
        os.rename(image, "./" + CRASHING_IMAGES_FOLDER + "/" + crashedFileName + ".img")
        main.outputFileNb += 1


if __name__ == "__main__":
    subprocess.Popen(['mkdir', CRASHING_IMAGES_FOLDER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)   # if dir doesn't exist program will crash
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser cancelled fuzzing.")


