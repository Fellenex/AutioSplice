#Timestamps module, written by Chris Keeler

import re

class Timestamp():
    def __init__(self, _hours, _minutes, _seconds):
        self.hours = _hours
        self.minutes = _minutes
        self.seconds = _seconds
        self.totalSeconds = _hours*60*60 + _minutes*60 + _seconds

    def toString(self):
        stampString = ""
        stampString += padInteger(self.hours)
        stampString += ":"
        stampString += padInteger(self.minutes)
        stampString += ":"
        stampString += padInteger(self.seconds)

        return stampString
        
#Creates a string of length 2 out of an integer < 100
def padInteger(_padMe):
    padded = ""
    if _padMe == 0:
        padded = "00"
    elif _padMe < 10:
        padded = "0"+str(_padMe)
    elif _padMe < 100:
        padded = str(_padMe)
    else:
        print "Integer is too large to pad: "+str(_padMe)
        padded = "60"

    return padded



#Tests each timestamp format available in the parseTimestamp() function
def testTimestamps():
    examps = ["00:24:32-00:24:38", "19:59-20:21", "002432-002438", "1959-2021"]
    timestamps = []
    for i in range(len(examps)):
        ts_one,ts_two = parseTimestamp(examps[i])
        timestamps.append(ts_one)
        timestamps.append(ts_two)

#Takes a string and creates two timestamps, from the start and ending points.
def parseTimestamp(_timestampString):
    #Note: All timestamp formats expect a character inbetween the starting and ending timestamps.

    #formats with the colons between the numbers, e.g. 00:24:32-00:24:38, or 19:59-20:21
    hmsc = r'\d\d:\d\d:\d\d.\d\d:\d\d:\d\d'
    msc = r'\d\d:\d\d.\d\d:\d\d'

    #formats without the colon between the numbers, e.g. 002432-002438, or 1959-2021
    hms = r'\d\d\d\d\d\d.\d\d\d\d\d\d'
    ms = r'\d\d\d\d.\d\d\d\d'

    #00:24:32-00:24:38
    if re.search(hmsc, _timestampString, flags=0):
        ts_one = Timestamp(int(_timestampString[0:2]), int(_timestampString[3:5]), int(_timestampString[6:8]))
        ts_two = Timestamp(int(_timestampString[9:11]), int(_timestampString[12:14]), int(_timestampString[15:17]))

    #19:59-20:21
    elif re.search(msc, _timestampString, flags=0):
        ts_one = Timestamp(0, int(_timestampString[0:2]), int(_timestampString[3:5]))
        ts_two = Timestamp(0, int(_timestampString[6:8]), int(_timestampString[9:11]))

    #002432-002438
    elif re.search(hms, _timestampString, flags=0):
        ts_one = Timestamp(int(_timestampString[0:2]), int(_timestampString[2:4]), int(_timestampString[4:6]))
        ts_two = Timestamp(int(_timestampString[7:9]), int(_timestampString[9:11]), int(_timestampString[11:13]))

    #1959-2021
    elif re.search(ms, _timestampString, flags=0):
        ts_one = Timestamp(0, int(_timestampString[0:2]), int(_timestampString[2:4]))
        ts_two = Timestamp(0, int(_timestampString[5:7]), int(_timestampString[7:9]))

    else:
        print "Unknown timestamp format."
        print "Use one of '00:24:32-00:24:38', '19:59-20:21', '002432-002438', or '1959-2021'"

    return ts_one, ts_two
