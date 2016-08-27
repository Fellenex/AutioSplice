#Main module, written by Chris Keeler

import math         #for fabs
import os           #for path.split
import sys          #for getting command-line arguments
from timestamps import *
from correctness import *


class Splice():
    def __init__(self, _ts_one, _ts_two, _sourceFilename, _destinationFilename):
        self.start = _ts_one.toString()
        self.end = _ts_two.toString()

        self.length = math.fabs(_ts_two.totalSeconds - _ts_one.totalSeconds)

        #These should be strings of the form <name>.{mp3,wav,...}
        self.sourceFilename = _sourceFilename
        self.destinationFilename = _destinationFilename

    #Creates a string which can be used as a command to create this splice as a file.
    #Full format should look like:
    #   ffmpeg -ss [start] -i in.xyz -f mp3 -t [duration] -strict -2 -c copy out.mp3
    #Format pieced together from:
        #http://superuser.com/questions/377343/cut-part-from-video-file-from-start-position-to-end-position-with-ffmpeg
        #http://stackoverflow.com/questions/31765674/ffmpeg-not-cutting-as-expected
    def generateCommand(self):
        return ["ffmpeg",
                "-ss", self.start,
                "-i", self.sourceFilename,
                "-f", "mp3",
                "-t", str(int(self.length)),
                "-strict", "-2",
                "-c", "copy", self.destinationFilename
                ]


#Take a file of timestamps and create the objects needed to create a spliced file
def createSplicesFromTimestamps(_timestampFilename, _audioFilename):
    with open(_timestampFilename, 'r') as f:
        lines = f.readlines()

    audioLength = getAudioLength(_audioFilename)
    audioFilenameExtless = os.path.splitext(_audioFilename)[0]

    splices = []
    for i in range(len(lines)):
        ts_one,ts_two = parseTimestamp(lines[i])

        if audioLength < ts_one.totalSeconds:
            print "Issue with timestamp file, can't start at "+str(ts_one.totalSeconds)+"seconds when the file is only "+str(audioLength)+" seconds long."

        splices.append(Splice(ts_one, ts_two, _audioFilename, audioFilenameExtless+"_splices\\"+str(i+1)+".mp3"))

    return splices


def main():
    if checkCommandLineArguments():
        sourceAudioFilename = sys.argv[1]
        timestampsFilename = sys.argv[2]

        getAudioLength(sourceAudioFilename)

        splices = createSplicesFromTimestamps(timestampsFilename, sourceAudioFilename)

        sourceAudioExtless,sourceAudioExt = os.path.splitext(sourceAudioFilename)

        if len(splices) > 0:
            spliceDirectoryName = sourceAudioExtless+"_splices"
            print spliceDirectoryName
            dirCommand = ["mkdir", spliceDirectoryName]
            safeCommand(dirCommand)

        print splices

        for splice in splices:
            spliceCommand = splice.generateCommand()
            safeCommand(spliceCommand)

    else:
        exit()

main()
