__author__ = 'andrew'
import os, os.path, math
from collections import defaultdict


"""
    OVERALL ALGORITHM:
    * First, populate inverted index like in previous lab, but update the TF (math.log10(len(self.invertedIndex[token][str(x)]))+1)
        value for each term: docId: list[0] as we traverse
    * Next, run setTFIDFandWeights to do math

    TODO: Normalize index, Build query system, fix any other cataclysms that show their head

"""

class weightedInvertedIndexModel:
    # new basic dictionary

    docLen = None
    invertedIndex = None

    def buildNNNIndex(self):
        self.invertedIndex = defaultdict()

        print("Loading Index...")
        self.populateInvertedIndexWithTermFrequency()

        print("Calculating NNN weights...")
        self.setNNNWeights()

    def buildLTCIndex(self):
        self.invertedIndex = defaultdict()

        print("Loading Index...")
        self.populateInvertedIndexWithTermFrequency()

        print("Calculating TFIDF weights...")
        self.setTFIDFandWeights()



    def getLengthOfCorpus(self):
        # get amount of files in data/clean
        DIR = 'data/clean'
        N = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        return N

    def setNNNWeights(self):
        N = self.getLengthOfCorpus()
        self.docLen = defaultdict(float)

        nonZero = 0
        zero = 0
        test = 0
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
                    test+=1
                    token = token.rstrip('\n')
                    self.invertedIndex[token][str(x)][0] = (len(self.dict[token][str(x)])-1)*(len(self.dict[token].keys()))

                file.close()

    def setTFIDFandWeights(self):
        N = self.getLengthOfCorpus()
        self.docLen = defaultdict(float)

        nonZero = 0
        zero = 0
        test = 0
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
                    test+=1
                    token = token.rstrip('\n')

                    self.invertedIndex[token][str(x)][0] *= math.log10(N/len(self.invertedIndex[token]))

                    if self.docLen.get(x, None) is not None:
                        self.docLen[token] *= (self.invertedIndex[token][str(x)][0] * self.invertedIndex[token][str(x)][0])
                    else:
                        self.docLen[token] = (self.invertedIndex[token][str(x)][0] * self.invertedIndex[token][str(x)][0])

                file.close()

    def populateInvertedIndexWithTermFrequency(self):

        # for each file in data/clean
        count = 0
        test = 0
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
                            self.invertedIndex[token][str(x)][0] = math.log10(len(self.invertedIndex[token][str(x)])-1)+1
                            count+=1
                        else:
                            self.invertedIndex[token][str(x)].append(1)
                            self.invertedIndex[token][str(x)].append(i)
                            self.invertedIndex[token][str(x)][0] = math.log10(len(self.invertedIndex[token][str(x)])-1)+1
                            count+=1
                    else:
                        self.invertedIndex[token] = defaultdict(list)
                        self.invertedIndex[token][str(x)].append(1)
                        self.invertedIndex[token][str(x)].append(i)
                        self.invertedIndex[token][str(x)][0] = math.log10(len(self.invertedIndex[token][str(x)])-1)+1
                        count+=1
                    i=i+1

                #close file
                file.close()

    def normalizeIndex(self):
        #somehow we are dividing by zero
        for token in self.invertedIndex:
            for docID in self.invertedIndex.get(token):
                #if math.pow(self.docLen[docID],.5) != 0:
                self.invertedIndex[token][docID][0] = (self.invertedIndex[token][docID][0]) / (math.pow(self.docLen[token],.5))
                #else:
                #    self.invertedIndex[token][docID][0] = 0

    def printInvertedIndex(self):
        print(self.invertedIndex)

    def printDocLength(self):
        for item in self.docLen:
            if self.docLen[item] == 0:
                print("ZERO ITEM")
            else:
                print(self.docLen[item])