#Correctness module, written by Chris Keeler

import sys
import re
import subprocess

#Checks to make sure that the command line arguments are a source audio filename and a source timestamps filename
def checkCommandLineArguments():
    anyReg = r'^.+\..*$'    #"something.xyz"
    txtReg = r'^.+\.txt$'   #"something.txt"
    goodFormatting = True

    #"python autiosplice.py help"
    if len(sys.argv) == 2 and sys.argv[1]=="help":
        print "Execute the script with something of the form: "
        print "\t python autiosplice.py greatSong.mp3 timestamps.txt"
        goodFormatting = False

    #hopefully "python autiosplice <audioFilename> <timestampsFilename>"
    elif len(sys.argv) == 3:
        audioFilename = sys.argv[1]
        timestampsFilename = sys.argv[2]
        if not(re.search(anyReg, audioFilename)):
            print "Incorrectly formatted audio filename: "+audioFilename
            goodFormatting = False

        if not(re.search(txtReg, timestampsFilename)):
            print "Incorrectly formatted timestamps filename: "+timestampsFilename
            goodFormatting = False

    else:
        print "Incorrectly gave "+str(len(sys.argv))+" arguments."
        print "Try using 'python autiosplice.py help'"
        goodFormatting = False

    return goodFormatting

#subprocess.call with extra overhead statements
def safeCommand(_command):
    safe = True
    try:
        print "You're getting me to run: "
        print "\t"+str(_command)
        code = subprocess.call(_command, shell=True)
        if code < 0:
            print "Child was terminated by signal "+str(code)
            safe = False
        else:
            print "Child returned "+str(code)

    except OSError as e:
        print str(e)
        safe = False

    return safe

#Gets the length of _fileName, in seconds.
def getAudioLength(_fileName):
    lengthRe = r'\d+'

    args = ["ffprobe", "-show_entries", "format=duration", "-i", _fileName]
    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    lengthOutput = popen.stdout.read()

    match = re.search(lengthRe, lengthOutput)

    return match.group(0)
