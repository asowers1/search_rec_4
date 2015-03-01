__author__ = 'andrew'
import os, os.path, math
from collections import defaultdict

class weightedInvertedIndexModel:
    # new basic dictionary

    docLen = None
    invertedIndex = None

    def __init__(self):
        self.invertedIndex = defaultdict()
        self.populateInvertedIndexWithTermFrequency()
        self.setTFIDFandWeights()

    def getLengthOfCorpus(self):
        # get amount of files in data/clean
        DIR = 'data/clean'
        N = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        return N

    def setTFIDFandWeights(self):
        N = self.getLengthOfCorpus()
        self.docLen = defaultdict(float)

        nonZero = 0
        zero = 0
        for x in range(1, N):
            # logic to get file name
            zeroLen = 7 - len(str(x))
            zeroString = ''
            for num in range(0, zeroLen):
                zeroString += "0"

            # open file

            if os.path.isfile("data/clean/" + zeroString + str(x) + ".txt"):
                file = open("data/clean/" + zeroString + str(x) + ".txt", "r")

                for token in file:
                    token = token.rstrip('\n')
                    if float(self.invertedIndex[token][str(x)][0]) == 0.0:
                        #print(token)
                        zero+=1
                    else:
                        nonZero+=1
                        self.invertedIndex[token][str(x)][0] = float(self.invertedIndex[token][str(x)][0]) * float(math.log(N/len(self.invertedIndex[token]),10))
                        print("VAL1: "+str(float(self.invertedIndex[token][str(x)][0]))+" VAL2: "+str(float(math.log(N/len(self.invertedIndex[token]),10))))
                        if self.docLen.get(str(x),None) is not None:
                            #self.docLen[str(x)] *=  float(self.invertedIndex[token][str(x)][0]) *  float(self.invertedIndex[token][str(x)][0])
                            self.docLen[str(x)] *= float(self.invertedIndex[token][str(x)][0]) * float(self.invertedIndex[token][str(x)][0])
                        else:
                            #self.docLen[str(x)]=1.0
                            self.docLen[str(x)] = float(self.invertedIndex[token][str(x)][0]) * float(self.invertedIndex[token][str(x)][0])

                file.close()
        print("ZERO: "+str(zero)+" NONZERO: "+str(nonZero))

    def populateInvertedIndexWithTermFrequency(self):

        # for each file in data/clean
        for x in range(1, self.getLengthOfCorpus()):

            # logic to get file name
            zeroLen = 7 - len(str(x))
            zeroString = ''
            for num in range(0, zeroLen):
                zeroString += "0"

            # open file

            if os.path.isfile("data/clean/" + zeroString + str(x) + ".txt"):
                file = open("data/clean/" + zeroString + str(x) + ".txt", "r")
                # create positional index
                i = 0
                for token in file:
                    token = token.rstrip('\n')
                    if self.invertedIndex.get(token, None) is not None:
                        if self.invertedIndex[token].get(str(x), None) is not None:
                            self.invertedIndex[token][str(x)].append(i)
                            self.invertedIndex[token][str(x)][0] = math.log(len(self.invertedIndex[token][str(x)])-1,10)+1
                        else:
                        self.invertedIndex[token][str(x)].append(1)
                            self.invertedIndex[token][str(x)].append(i)
                    else:
                        self.invertedIndex[token] = defaultdict(list)
                        self.invertedIndex[token][str(x)].append(1)
                        self.invertedIndex[token][str(x)].append(i)
                    i=i+1

                #close file
                file.close()


    def printInvertedIndex(self):
        print(self.invertedIndex)

    def printDocLength(self):
        print(self.docLen)