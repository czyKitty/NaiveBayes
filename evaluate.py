import os
import sys
import re

#return attribute and data
def getData(dataFile):
    attribute = ""
    data = []
    aCount = 0
    dataSet = open(dataFile,'r')
    line = dataSet.readline()
    while(line[:-1] != "@data"):
        if line[:10] == "@attribute":
            attribute += line
            aCount += 1
        line = dataSet.readline()

    while(line != ''):
        if len(line.split(',')) == aCount:
            data.append(line)
        line = dataSet.readline()

    return(attribute,data)

def getResult(actualResult, threshold):
    result = open("result.txt",'r')
    line = re.split(':| ',result.readline())
    classType = []
    for i in range(len(line)//2):
        classType.append(line[2*i+1])
    
    confusMatrix = [[0 for x in range(len(classType))] for y in range(len(classType))]

    count = 0
    while(len(line) > 1):
        #treat each class as positive
        for i in range(len(classType)):
            #when larger than threshold,
            if line[0] == actualResult[i]:
                confusMatrix[i][i] += 1
            else:
                confusMatrix[classType.index(line[0])][i] += 1
        line = re.split(':| ',result.readline())
        count += 1
    showResult(confusMatrix,classType[:-1])
    result.close()

def showResult(confusMatrix, classType):
    print("##########################################")
    print("======confusing matrix=======")
    printline = "      "
    for i in range(len(classType)):
        printline += classType[i]+"  "
    print(printline)
    for i in range(len(classType)):
        printline = ""
        printline += str(classType[i])+"   "
        for j in range(len(classType)):
            printline += str(confusMatrix[j][i])+"  "
        print(printline)


def main():
    dataFile = sys.argv[1]
    
    actualResult = []

    threshold = 0.5
    if len(sys.argv) == 3:
        threshold = float(sys.argv[2])

    result = getData(dataFile)
    if os.path.exists("result.txt"):
        os.remove("result.txt")

    for i in range(len(result[1])):
        validationFile = open("validation.txt",'w')
        trainingFile = open("training.txt",'w')
        validationFile.write(result[0]+'\n'+"@data\n"+result[1][i])
        actualResult.append(result[1][i].split(',')[-1][:-1])
        trainingFile.write(result[0]+'\n'+"@data\n")
        for j in range(len(result[1])):
            if j != i:
                trainingFile.write(result[1][j])
        validationFile.close()
        trainingFile.close()
        os.system('python3 naivebayes.py training.txt validation.txt result.txt')
    getResult(actualResult,threshold)
main()