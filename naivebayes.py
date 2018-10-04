import sys
import copy
import operator

#take the name of training data file and return a list of probability for each possible prediction in train data
def trainBayes(trainFile):
    trainData = open(trainFile,'r')
    line = trainData.readline().replace("{",'').split()
    classType = []
    datalist = []
    propDict = {}
    attribDict = {}
    #create map for each attribute and store them in list
    while(line[0] != "@data"):
        attribDict = {}
        newLine = trainData.readline()
        #not the last attribute
        if line[0] == "@attribute" and len(newLine) > 1:
            for i in range(2,len(line)):
                attribDict.update({line[i][:-1]:0})
            datalist.append(attribDict)
        #last attribute -> class to predict
        elif line[0] == "@attribute":
            for i in range(2,len(line)):
                attribDict.update({line[i][:-1]:0})
                classType.append(line[i][:-1])
                propDict.update({line[i][:-1]:0})
            for item in datalist:
                for key in item.keys():
                    item[key] = copy.deepcopy(attribDict)
        #skip empty lines
        while(len(newLine)<=1):
            newLine = trainData.readline()
        line = newLine.replace("{",'').split()

    #count how many time each property appears
    count = 0
    line = trainData.readline()
    while(line != ''):
        count += 1
        tempLine = line[:-1].split(',')
        for i in range(len(datalist)):
            datalist[i][tempLine[i]][tempLine[-1]] += 1
        propDict[tempLine[-1]] += 1
        attribDict[tempLine[-1]] += 1
        line = trainData.readline()
    #calculate probability for each property
    for i in range(len(datalist)):
        for prop in datalist[i]:
            for item in datalist[i][prop]:
                datalist[i][prop][item] = float(datalist[i][prop][item])/float(propDict[item])

    #calculate over all probability
    for item in attribDict:
        attribDict[item] = float(attribDict[item])/float(count)

    trainData.close()
    return(datalist, attribDict,classType)

#use the training data for prediction
def predictBayes(classType, datalist, problist, inputFile, outputFile):
    #read the inputFile and use prob to predict
    inputData = open(inputFile,'r')
    outputData = open(outputFile,'a')
    line = inputData.readline()
    while(line[:-1] != "@data"):
        line = inputData.readline()
    line = inputData.readline().split(',')[:-1]
    #record probability for each choice
    while(len(line) >= 1):
        resultDict = {}
        #set each probability to 1
        for item in problist:
            resultDict.update({item:1})
        #do naive bayes!
        for item in resultDict:
            for i in range(len(line)):
                resultDict[item] *= datalist[i][line[i]][item]
            resultDict[item] *= problist[item]
        line = inputData.readline().split(',')[:-1]
        evidence = 0
        for item in resultDict:
            evidence += resultDict[item]
        outputData.write(max(resultDict,key=resultDict.get)+" ")
        for i in range(len(classType)):
            outputData.write(classType[i]+":"+str(format(round(resultDict[classType[i]]/evidence,2),'.2f'))+" ")
        outputData.write("\n")


#loop and read input file
def main():
    trainFile = sys.argv[1]
    inputFile = sys.argv[2]
    outputFile = sys.argv[3]

    data = trainBayes(trainFile)
    predictBayes(data[2],data[0],data[1],inputFile,outputFile)
main()