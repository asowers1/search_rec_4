__author__ = 'andrew'
import weightedInvertedIndexModel
import re
from collections import defaultdict
import math

class rankedRetrivalController:

    rRController = None
    database     = None
    smartVarientDoc = None
    smartVarientQuery = None

    def __init__(self):
        print("Supported SMART variants: [n,l][n,t][n,c] (default is 'ltc')\n")
        self.smartVarientDoc = input("Please enter SMART variant for documents:")
        self.smartVarientQuery = input("Please enter SMART variant for queries:")
        self.rRController = weightedInvertedIndexModel.weightedInvertedIndexModel()

        self.queryIngest()

    def queryIngest(self):
        if (self.smartVarientDoc == "ltc"):
            self.indexltc()
        elif (self.smartVarientDoc == "nnn"):
            self.indexnnn()
        else:
            print("error in index type")
            return

        if (self.smartVarientQuery == "ltc"):
            self.ltcQuery()
        elif (self.smartVarientQuery == "nnn"):
            self.nnnQuery()
        else:
            print("error in query type")
            return


    def indexltc(self):
        self.rRController.buildLTCIndex()

    def indexnnn(self):
        self.rRController.buildNNNIndex()

    def ltcQuery(self):
        query = ""
        while query is not "QUIT":
            query = input("Enter Query or 'QUIT':")

            strippedpunc = self.removePunc(query)
            queryTokenList = strippedpunc.split(" ")
            self.removeUpperFromObject(queryTokenList)
            print(queryTokenList)

            queryDictionary = defaultdict()
            for term in queryTokenList:
                if term not in queryDictionary:
                    queryDictionary[term] = 1
                else:
                    queryDictionary[term] += 1

            for key in queryDictionary.keys():
                termFrequency = 1 + math.log10(queryDictionary[key])
                inverseDocumentFrequency = 1 + math.log10(self.rRController.getLengthOfCorpus()/(len(self.rRController.invertedIndex.keys())))
                queryDictionary[key] = termFrequency * inverseDocumentFrequency


    def nnnQuery(self):
        query = ""
        while query is not "QUIT":
            query = input("Enter Query or 'QUIT':")

            strippedpunc = self.removePunc(query)
            queryTokenList = strippedpunc.split(" ")
            self.removeUpperFromObject(queryTokenList)
            print(queryTokenList)

            queryDictionary = defaultdict()
            for term in queryTokenList:
                if term not in queryDictionary:
                    queryDictionary[term] = 1
                else:
                    queryDictionary[term] += 1

    def removePunc(self, string):
        string = re.sub(re.compile("[^-.\"'\w\s]",re.DOTALL ) ,"" ,string) # remove all occurances punctuation
        return string

    def removeUpperFromObject(self, objects):
        for i in range(len(objects)):
            objects[i] = objects[i].lower()

        return objects