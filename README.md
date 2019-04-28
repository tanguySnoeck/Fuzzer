# LINGI2347GroupWork1

Computer System Security 

If you do not have the access rights needed to run the converter tool, you might want to run the rights.sh script:

    sudo bash rights.sh


If this still does not fix the problem, you might want to use the converter_static rather than the simple converter
Change the line 122 of generation.py into the following line:

    pipes = subprocess.Popen(['../converter_static', image , 'outputImage'], stderr=subprocess.PIPE)


To run the fuzzer, use one of the following command: (when in the generation folder)

    python3 generation.py [number of files generated]

    python generation.py [number of files generated]

When running the fuzzer with 500 as the number of files generated, I manage to consistently obtain 5 different errors.