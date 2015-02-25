__author__ = 'andrew'
import os, os.path
from collections import defaultdict
import pprint

class InvertedIndexModel:

    # new basic dictionary
    def __init__(self):
        self.invertedIndex = defaultdict()
        self.populateInvertedIndex()

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
                        self.invertedIndex[token][str(x)].append(i)
                    else:
                        self.invertedIndex[token] = defaultdict(list)
                        self.invertedIndex[token][str(x)].append(i)
                    i=i+1
                #close file
                file.close()


    def printInvertedIndex(self):
        print(self.invertedIndex)

