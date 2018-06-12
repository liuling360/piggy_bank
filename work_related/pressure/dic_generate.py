#! encoding: utf8

import re
import sys

def GetMiddleStr(content,startStr,endStr):
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    print str(startIndex) + " : " + str(endIndex)
    return content[startIndex:endIndex]

def getMiddleStr2(content):
    return re.findall(r'.*Request\((.*)\).*', content)[0]


def main(file_name):
    file_open = open(file_name, "r")
    file_open_write = open("generate_dic/" + "output.log" + "_output", "a")

    for line in file_open.readlines():
        if "Request" in line and ("mxbeta_version_5_0" in line) and "interfaceNewName" in line and "test" not in line:
            if "Filmy Duniya" in line or "Devotion" in line or "News" in line or "Featured" in line or "TV Shows & Drama" in line or "Toons" in line:
            #result = GetMiddleStr(line, "Request(", ")")
                result = getMiddleStr2(line)
                file_open_write.write(result+"\n")

    file_open_write.close()
    file_open.close()

if __name__ == '__main__' :
    file_name = sys.argv[1]
    print file_name
    main(file_name)