#!/usr/bin/python3

import sys
import subprocess
import os
import struct
from random import randint
from shutil import copyfile

CRASHING_IMAGES_FOLDER = "mutationCrash"

def main():
    if (len(sys.argv) != 5):
        print("Usage: " + sys.argv[0] + " [inputFile] [nbOfTestRuns] [nbOfModifications] [percentageOfBytesToModify]")
        exit(1)

    #initialising the main function
    main.correctImage = sys.argv[1]
    nbTestRuns = int(sys.argv[2])
    maxModififications = int(sys.argv[3])
    percentageModification = float(sys.argv[4])
    inputFileSize = os.path.getsize(main.correctImage)
    
    nbOfBytesToModify = round(inputFileSize * percentageModification)
    
    main.hasCrashed = False
    main.outputFileNb = 0

    print("Started fuzzing ! \nAll crashing input files will be put in the folder '" + CRASHING_IMAGES_FOLDER + "'.")
    for x in range(1, nbTestRuns):
        print("Test n°",str(x),sep='',end="\r",flush=True)
        try:
            with open(main.correctImage, 'r+b') as file:
                for y in range(maxModififications):
                    # once the image is broken, exits the for loop
                    if (main.hasCrashed): 
                        break

                    # modifies the image file
                    for z in range(nbOfBytesToModify):
                        file.seek(randint(0, inputFileSize))
                        file.write(randint(0, 128).to_bytes(1, 'little'))
    
                    # tests the image
                    testImage(main.correctImage)

        except FileNotFoundError:
            print("The file '" + main.correctImage + "' does not exists, aborting.")
            exit(1)

        # resetting the variable
        main.hasCrashed = False
    print("\n Fuzzing over, found " + str(main.outputFileNb) + " crashing input files.")

def testImage(image):
    try:
        # testing the file using the converter tool 
        pipes = subprocess.Popen(['../converter', image, 'outputImage'], stderr=subprocess.PIPE)
        #pipes = subprocess.Popen(['../converter_static', image, 'outputImage'], stderr=subprocess.PIPE)
        std_err = pipes.communicate()

        # if the program crashes
        if (pipes.returncode != 0 and std_err[1].decode("utf-8").find('crashed')):
            os.rename(image, "./" + CRASHING_IMAGES_FOLDER + "/testinput" + str(main.outputFileNb) + ".img")
            main.outputFileNb += 1
            main.hasCrashed = True
            copyfile("../testinput.img", main.correctImage)

    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    subprocess.Popen(['mkdir', CRASHING_IMAGES_FOLDER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)   # if dir doesn't exist program will crash
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser cancelled fuzzing.")
