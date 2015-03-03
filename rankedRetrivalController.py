__author__ = 'andrew'
import weightedInvertedIndexModel
import re
from collections import defaultdict
import math
import operator
import Database

class rankedRetrivalController:

    rRController = None
    database     = None
    smartVarientDoc = None
    smartVarientQuery = None

    def __init__(self):
        self.database = Database.WebDB("data/cache/database.db")
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
            #print(queryTokenList)

            queryDictionary = defaultdict(float)
            for term in queryTokenList:
                if term not in queryDictionary:
                    queryDictionary[term] = 1
                else:
                    queryDictionary[term] += 1

            qlength = 0
            for key in queryDictionary.keys():
                termFrequency = 1 + math.log10(queryDictionary[key])
                inverseDocumentFrequency = math.log10(self.rRController.getLengthOfCorpus()/(len(self.rRController.invertedIndex[key])))
                print("TERM FREQ: "+str(termFrequency)+" INVER DOC FREQ: "+str(inverseDocumentFrequency)+" lEN INVERTED INDEX: " + str(len(self.rRController.invertedIndex)))

                queryDictionary[key] = termFrequency * inverseDocumentFrequency
                qlength += queryDictionary[key] * queryDictionary[key]

            for key in queryDictionary.keys():
                queryDictionary[key] = queryDictionary[key]/math.sqrt(qlength)

            self.getWeightedResults(queryDictionary)


    def nnnQuery(self):
        query = ""
        while query != "QUIT":
            query = input("Enter Query or 'QUIT':")
            print()

            strippedpunc = self.removePunc(query)
            queryTokenList = strippedpunc.split(" ")
            self.removeUpperFromObject(queryTokenList)

            queryDictionary = defaultdict()
            for term in queryTokenList:
                if term not in queryDictionary:
                    queryDictionary[term] = 1
                else:
                    queryDictionary[term] += 1

            self.getWeightedResults(queryDictionary)

    def removePunc(self, string):
        string = re.sub(re.compile("[^-.\"'\w\s]",re.DOTALL ) ,"" ,string) # remove all occurances punctuation
        return string

    def removeUpperFromObject(self, objects):
        for i in range(len(objects)):
            objects[i] = objects[i].lower()

        return objects

    def getWeightedResults(self, queryDictionary):
        resultDocIDlist = []

        for term in queryDictionary:
            docIDList = []
            docDictionary = defaultdict()
            docDictionary = self.rRController.getDocIDsFromTerm(term)
            for docID in docDictionary:
                docIDList.append(docID)

            if len(resultDocIDlist) == 0:
                resultDocIDlist = docIDList
            else:
                resultDocIDlist = set(resultDocIDlist) & set(docIDList)

        documentWeights = defaultdict(int)
        for term in queryDictionary:
             for docID in resultDocIDlist:
                 documentWeights[docID] += self.rRController.invertedIndex[term][docID][0] * queryDictionary[term]

        self.printOrderedResults(documentWeights)

    def printOrderedResults(self, finalResult):
        orderedTupples = sorted(finalResult.items(), key=operator.itemgetter(1))
        orderedTupples.reverse()

        print("\nItem Search Results:")
        i = 1
        for id in orderedTupples:
            if i == 4:
                break
            result = self.database.getInfoByID(id[0])
            print(str(i)+". "+result[0][2]+": "+self.database.getItemByID(id[0])+" ("+str(id[1])+")\n")
            i+=1

        print("\n")
        i = 1
        for id in orderedTupples:
            if i == 4:
                break
            result = self.database.getInfoByID(id[0])
            url = result[0][0]
            title = result[0][1]
            type = result[0][2]
            name = self.database.getItemByID(id[0])
            weight = str(id[1])
            print(str(i) + ".\t" + title + "\t(" + weight + ")\n\t" + url + "\n\t" + type + ": " + name + "\n")
            i+=1

