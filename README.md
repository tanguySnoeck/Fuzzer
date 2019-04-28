# LINGI2347GroupWork1

Computer System Security 

Group members:
Clément Caroff, Jacques-Antoine Portal, Tanguy Snoeck.

## Executing our code:
(The code was written entirely on Linux systems)

If you do not have the <b>access rights</b> needed to run the converter tool, you might want to run the rights.sh script:

    sudo bash rights.sh


If this still does not fix the problem, you might want to use the <b>converter_static</b> rather than the simple converter.<br>
Change the python fuzzer file to use the following line:

    pipes = subprocess.Popen(['../converter_static', image, 'outputImage'], stderr=subprocess.PIPE)

Rather than:<br>
For the mutation fuzzer: line 58<br>
For the generation based fuzzer: line 169<br>

To run the <b>mutation fuzzer</b>, open a terminal window from the mutation folder and use one of the following commands:

    python3 mutation.py [inputFile] [nbOfTestRuns] [nbOfModifications] [percentageOfBytesToModify]

    python mutation.py [inputFile] [nbOfTestRuns] [nbOfModifications] [percentageOfBytesToModify]

You can play with the arguments to see which ones work best and generate files that crash the converter.

To run the <b>generation fuzzer</b>, open a terminal window from the generation folder and use one of the following commands:

    python3 generation.py [number of files generated]

    python generation.py [number of files generated]

## Crash:

When running the fuzzer with 1000 as the number of files generated, we manage to consistently obtain 4 different errors.

The first error that was found when making the fuzzer was when the version number was between 20 and 29 (in base 10). To find such a file in the generationCrash directory, you can search for "v2" and you should find at least a few .img files that start with v20 or v21, or v22 ... v29. At first, we thought of using numbers higher than 100, however this did not make the tool crash.

The second error was found much later when making the fuzzer, it involves the author name, and basically, sometimes, when making a file that does not finish the author name by a 00 (hex), and the file not having any 00 soon after, the converter seems to crash with an "xxx stack smashing detected xxx: ../converter terminated" error. Sometimes, this error gets even worse and prints a lot more information:


```
* stack smashing detected *: ../converter terminated
======= Backtrace: =========
/lib/x86_64-linux-gnu/libc.so.6(+0x70bfb)[0x7f1e4b2d6bfb]
/lib/x86_64-linux-gnu/libc.so.6(__fortify_fail+0x37)[0x7f1e4b35f437]
/lib/x86_64-linux-gnu/libc.so.6(__fortify_fail+0x0)[0x7f1e4b35f400]
../converter[0x401335]
/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf1)[0x7f1e4b2862e1]
../converter[0x4008d9]
======= Memory map: ========
00400000-00402000 r-xp 00000000 08:07 1860833                            /home/jack/Documents/lingi2347groupwork1/converter
00601000-00602000 r--p 00001000 08:07 1860833                            /home/jack/Documents/lingi2347groupwork1/converter
00602000-00603000 rw-p 00002000 08:07 1860833                            /home/jack/Documents/lingi2347groupwork1/converter
01f0e000-01f2f000 rw-p 00000000 00:00 0                                  [heap]
7f1e4b04f000-7f1e4b065000 r-xp 00000000 08:07 2223876                    /lib/x86_64-linux-gnu/libgcc_s.so.1
7f1e4b065000-7f1e4b264000 ---p 00016000 08:07 2223876                    /lib/x86_64-linux-gnu/libgcc_s.so.1
7f1e4b264000-7f1e4b265000 r--p 00015000 08:07 2223876                    /lib/x86_64-linux-gnu/libgcc_s.so.1
7f1e4b265000-7f1e4b266000 rw-p 00016000 08:07 2223876                    /lib/x86_64-linux-gnu/libgcc_s.so.1
7f1e4b266000-7f1e4b3fb000 r-xp 00000000 08:07 2225212                    /lib/x86_64-linux-gnu/libc-2.24.so
7f1e4b3fb000-7f1e4b5fb000 ---p 00195000 08:07 2225212                    /lib/x86_64-linux-gnu/libc-2.24.so
7f1e4b5fb000-7f1e4b5ff000 r--p 00195000 08:07 2225212                    /lib/x86_64-linux-gnu/libc-2.24.so
7f1e4b5ff000-7f1e4b601000 rw-p 00199000 08:07 2225212                    /lib/x86_64-linux-gnu/libc-2.24.so
7f1e4b601000-7f1e4b605000 rw-p 00000000 00:00 0 
7f1e4b605000-7f1e4b628000 r-xp 00000000 08:07 2225205                    /lib/x86_64-linux-gnu/ld-2.24.so
7f1e4b808000-7f1e4b80a000 rw-p 00000000 00:00 0 
7f1e4b827000-7f1e4b828000 rw-p 00000000 00:00 0 
7f1e4b828000-7f1e4b829000 r--p 00023000 08:07 2225205                    /lib/x86_64-linux-gnu/ld-2.24.so
7f1e4b829000-7f1e4b82a000 rw-p 00024000 08:07 2225205                    /lib/x86_64-linux-gnu/ld-2.24.so
7f1e4b82a000-7f1e4b82b000 rw-p 00000000 00:00 0 
7ffc396ef000-7ffc39710000 rw-p 00000000 00:00 0                          [stack]
7ffc39753000-7ffc39755000 r--p 00000000 00:00 0                          [vvar]
7ffc39755000-7ffc39757000 r-xp 00000000 00:00 0                          [vdso]
ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]

```
(to find the files that crashed because of this, search for true in the generationCrash folder).

We discovered the following crashes by the fuzzer generating author names that contained 00, hence shifting what the tool considered the width, height and number of colours.

The third kind of crashing files found was when the height of an image (the one in the parameters, not the real height of the file) is (in base 10) larger than approximately 2100000000. This might be due to the fact that positive 32 bits values stop at 2147483647, and higher values are interpreted as negative values, which makes the converter tool crash. (to find these files, search for ones with a large number after _l in the file name)

Using negative values as the number of colours also crashes the converter (which is the fourth kind of crash we found). At first, we thought of using a number of colours higher than 256, however that was handled by the tool. (to find these files, search for ones with a large number after _nc in the file name)

We have provided 4 example files in the example file zip folder, one for each of the crashes we found.

## The last / fifth possible problem...

It seemed that using a "small length" and a negative number of colours, or the opposite was the way to produce the most crashing files. Using negative numbers for both seems to reduce the number of crashing files generated. This might be a clue to finding a 5th way of crashing the converter. However, we could not build a fuzzer that would consistently produce such kind of crashes.

Finally, we noticed that the only parameter that seems not to cause some crashes was the width. This is suspicious but we could not find consistent crashes with the width. This would be another clue to find a 5th crash.

Our generation fuzzer tests for a few more possible problems but none seems to cause any crash. We test for non-matching length, width and number of colours, we try to use colours that are not 32 bit values, that did nothing, and tried using negative widths and it did nothing either.
