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
    inputFileSize = os.path.getsize(correctImage)
    
    nbOfBytesToModify = round(inputFileSize * percentageModification)
    
    main.hasCrashed = False
    main.outputFileNb = 0

    print("Started fuzzing ! \nAll crashing input files will be put in the folder 'crashingImages'.")

    for x in range(1, nbTestRuns):
        print ("Test run n°" + str(x) + " ...")

        try:
            with open(correctImage, 'r+b') as file:
                for y in range(maxModififications):
                    if (main.hasCrashed): break

                    for z in range(nbOfBytesToModify):
                        file.seek(randint(0, inputFileSize))
                        file.write(randint(0, 128).to_bytes(1, 'little'))
    
                    testImage(correctImage)
                
                if (not main.hasCrashed):
                    print("Did maximum number of modifications on the file, giving up and starting new test run.")
        except FileNotFoundError:
            print("The file '" + correctImage + "' does not exists, aborting.")
            exit(1)

        main.hasCrashed = False
    
    print("Fuzzing over, found " + str(main.outputFileNb) + " crashing input files.")

def testImage(image):
    try:
        pipes = subprocess.Popen(['sudo', '../converter', image, 'outputImage'], stderr=subprocess.PIPE)
        std_err = pipes.communicate()

        if (pipes.returncode != 0 and std_err[1].decode("utf-8").find('crashed')):
            print("Found a bug !")
            os.rename(image, "crashingImages/testinput" + str(main.outputFileNb) + ".img")
            main.outputFileNb += 1
            main.hasCrashed = True
            copyfile("../testinput.img", "testinput.img")
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser cancelled fuzzing.")