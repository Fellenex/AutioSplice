#Main module, written by Chris Keeler

#Should be executed as:
    #python autiosplice.py <source_audio/video> <timestamps_file>

import os           #for path.split
import sys          #for getting command-line arguments
from timestamps import *
from correctness import *


class Splice():
    #Parameters:
    #   _ts_one, _ts_two: A Timestamp object
    #   _sourceFilename: A string, representing the splice's source audio file
    #   _destinationFilename: A string, representing the location at which to save this splice
    def __init__(self, _ts_one, _ts_two, _sourceFilename, _destinationFilename):
        self.start = _ts_one.toString()
        self.end = _ts_two.toString()

        self.length = _ts_two.totalSeconds - _ts_one.totalSeconds

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
#Parameters:
#   _timestampFilename: A string, representing the location of the timestamp file
#   _audioFilename: A string, representing the location of the source audio file
#Return Value:
#   splices: A list of Splice objects, one for each pair of timestamps in the timestamp file.
#
def createSplicesFromTimestamps(_timestampFilename, _audioFilename):
    audioLength = getAudioLength(_audioFilename)
    audioFilenameExtless = os.path.splitext(_audioFilename)[0]
    splices = []

    with open(_timestampFilename, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        ts_one,ts_two = parseTimestamp(lines[i])

        #If the second timestamp is later than the total length of the audio, then there's no way to create this splice.
        assert ts_two.totalSeconds < audioLength

        #If the second timestamp is earlier than the first timestamp, then there's no way to create this splice.
        assert ts_one.totalSeconds < ts_two.totalSeconds

        #Because ts_one.totalSeconds < ts_two.totalSeconds, and ts_two.totalSeconds < audioLength,
        #   we have ts_one.totalSeconds < audioLength

        splices.append(Splice(ts_one, ts_two, _audioFilename, audioFilenameExtless+"_splices\\"+str(i+1)+".mp3"))

    return splices


def main():
    checkForHelp()
    
    assert checkCommandLineArguments()

    sourceAudioFilename = sys.argv[1]
    timestampsFilename = sys.argv[2]
    sourceAudioExtless,sourceAudioExt = os.path.splitext(sourceAudioFilename)

    splices = createSplicesFromTimestamps(timestampsFilename, sourceAudioFilename)
    assert len(splices) > 0

    #Create the directory where everything is saved
    spliceDirectoryName = sourceAudioExtless+"_splices"
    dirCommand = ["mkdir", spliceDirectoryName]
    safeCommand(dirCommand)

    #Create the splice files themselves
    for splice in splices:
        spliceCommand = splice.generateCommand()
        safeCommand(spliceCommand)

main()
