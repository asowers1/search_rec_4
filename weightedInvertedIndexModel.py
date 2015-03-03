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
        self.populateInvertedIndex()

        print("Calculating NNN weights...")
        self.setNNNWeights()

    def buildLTCIndex(self):
        self.invertedIndex = defaultdict()

        print("Loading Index...")
        self.populateInvertedIndex()

        print("Calculating TFIDF weights...")
        self.setTFIDFandWeights()

        print("Normalizing index...")
        self.normalizeIndex()




    def getLengthOfCorpus(self):
        # get amount of files in data/clean
        DIR = 'data/clean'
        N = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        return N-1

    def setNNNWeights(self):
        for token in self.invertedIndex:
            for docID in self.invertedIndex[token]:
                self.invertedIndex[token][docID][0] = (len(self.invertedIndex[token][docID])-1)

    def setTFIDFandWeights(self):
        N = self.getLengthOfCorpus()
        self.docLen = defaultdict(float)
        for token in self.invertedIndex:
            for docID in self.invertedIndex[token]:
                self.invertedIndex[token][docID][0] = (1+math.log10(len(self.invertedIndex[token][docID])-1))*math.log10(N/len(self.invertedIndex[token]))
                if self.docLen.get(docID, None) is not None:
                    self.docLen[docID] += (self.invertedIndex[token][docID][0] * self.invertedIndex[token][docID][0])
                else:
                    self.docLen[docID] = (self.invertedIndex[token][docID][0] * self.invertedIndex[token][docID][0])


    def populateInvertedIndex(self):

        # get amount of files in data/clean
        DIR = 'data/clean'
        length = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

        # for each file in data/clean
        for x in range(1, length):

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
                        if self.invertedIndex[token].get(str(x),None) is not None:
                            self.invertedIndex[token][str(x)].append(i)
                        else:
                            self.invertedIndex[token][str(x)].append(0)
                            self.invertedIndex[token][str(x)].append(i)
                    else:
                        self.invertedIndex[token] = defaultdict(list)
                        self.invertedIndex[token][str(x)].append(0)
                        self.invertedIndex[token][str(x)].append(i)
                    i=i+1
                #close file
                file.close()

    def getDocIDsFromTerm(self, term):
        return self.invertedIndex[term]

    def normalizeIndex(self):
        #somehow we are dividing by zero
        for token in self.invertedIndex:
            for docID in self.invertedIndex[token]:
                self.invertedIndex[token][docID][0] = (self.invertedIndex[token][docID][0]) / (math.sqrt(self.docLen[docID]))

    def printInvertedIndex(self):
        print(self.invertedIndex)

    def printDocLength(self):
        for item in self.docLen:
            if self.docLen[item] == 0:
                print("ZERO ITEM")
            else:
                print(self.docLen[item])