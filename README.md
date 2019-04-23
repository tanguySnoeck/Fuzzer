# LINGI2347GroupWork1

Computer System Security 

If you do not have the access rights needed to run the converter tool, you might want to run the rights.sh script:
    sudo bash rights.sh
</br>
If this still does not fix the problem, you might want to use the converter_static rather than the simple converter
Change the line 122 of generation.py into the following line:
        pipes = subprocess.Popen(['../converter_static', image , 'outputImage'], stderr=subprocess.PIPE)