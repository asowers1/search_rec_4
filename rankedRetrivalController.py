__author__ = 'andrew'
import weightedInvertedIndexModel
from collections import defaultdict
import math
import operator
import Database
import nltk
import nltk.data
import re
import Evaluation
import random

class rankedRetrivalController:

    rRController = None
    database     = None
    smartVarientDoc = None
    smartVarientQuery = None
    currentQuery = None
    evaluator = None;
    resultsList = list()
    automated = False
    randomOrder = False

    def __init__(self, automated):
        self.database = Database.WebDB("data/cache/database.db")
        self.evaluator = Evaluation.Evaluation()
        if automated == True:
            self.automated = automated
            self.automatedQuery("nnn","nnn")
            self.automatedQuery("nnn","ltc")
            self.automatedQuery("ltc","nnn")
            self.automatedQuery("ltc","ltc")
            self.randomOrder = True
            self.automatedQuery("ltc","ltc")
        else:
            self.manualQuery()

    def automatedQuery(self, smartVarientDoc, smartVarientQuery):
        self.smartVarientDoc = smartVarientDoc
        self.smartVarientQuery = smartVarientQuery
        self.setIndexInstance()
        self.setIndex()
        list = self.database.listAllItems()
        #print("LIST: "+str(list))
        if smartVarientQuery is "ltc":
            for item in list:
                self.ltcQueryAutomated(item[0])
        elif smartVarientQuery is "nnn":
            for item in list:
                self.automatedNnnQuery(item[0])
        self.evaluator.printFinalAdverages()
        self.evaluator = Evaluation.Evaluation()

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    def manualQuery(self):
        print("Supported SMART variants: [n,l][n,t][n,c] (default is 'ltc')\n")
        self.smartVarientDoc = input("Please enter SMART variant for documents:")
        self.smartVarientQuery = input("Please enter SMART variant for queries:")
        self.setIndexInstance()
        self.queryIngest()

    def setIndexInstance(self):
        self.rRController = weightedInvertedIndexModel.weightedInvertedIndexModel()

    def setIndex(self):
        if (self.smartVarientDoc == "ltc"):
            self.indexltc()
        elif (self.smartVarientDoc == "nnn"):
            self.indexnnn()
        else:
            print("error in index type")
            return


    def queryIngest(self):

        self.setIndex()

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


    def ltcQueryAutomated(self, query):
        self.currentQuery = query
        strippedpunc = self.removePuncAndTokenize(query)
        queryTokenList = strippedpunc.split(" ")

        queryDictionary = defaultdict(float)
        for term in queryTokenList:
            if term not in queryDictionary:
                queryDictionary[term] = 1
            else:
                queryDictionary[term] += 1

        qlength = 0
        for key in queryDictionary.keys():
            termFrequency = 1 + math.log10(queryDictionary[key])
            inverseDocumentFrequency = math.log10(self.rRController.getLengthOfCorpus()/1+(len(self.rRController.invertedIndex[key])))
            queryDictionary[key] = termFrequency * inverseDocumentFrequency
            qlength += queryDictionary[key] * queryDictionary[key]



        for key in queryDictionary.keys():
            queryDictionary[key] = queryDictionary[key]/math.sqrt(qlength)

        #print(queryDictionary)


        self.getWeightedResults(queryDictionary)


    def ltcQuery(self):
        query = ""
        while True:
            query = input("Enter Query or 'QUIT':")
            if query == "QUIT":
                break
            self.ltcQueryAutomated(query)


    def automatedNnnQuery(self, query):
        self.currentQuery = query

        strippedpunc = self.removePuncAndTokenize(query)
        queryTokenList = strippedpunc.split(" ")
        self.removeUpperFromObject(queryTokenList)

        queryDictionary = defaultdict()
        for term in queryTokenList:
            if term not in queryDictionary:
                queryDictionary[term] = 1
            else:
                queryDictionary[term] += 1

            self.getWeightedResults(queryDictionary)
    def nnnQuery(self):
        query = ""
        while True:
            query = input("Enter Query or 'QUIT':")
            if query == "QUIT":
                break
            self.automatedNnnQuery(query)

    def removePuncAndTokenize(self, string):
        string = re.sub(re.compile("[^-.\"'\w\s]",re.DOTALL ) ,"" ,string) # remove all occurances punctuation
        string = self.removeUpperFromObject(nltk.word_tokenize(string))
        return " ".join(string)

    def removeUpperFromObject(self, objects):
        for i in range(len(objects)):
            objects[i] = objects[i].lower()

        return objects

    def getWeightedResults(self, queryDictionary):
        resultDocIDlist = []
        documentWeights = defaultdict(float)

        for term in queryDictionary:
            docDictionary = self.rRController.getDocIDsFromTerm(term)
            for docID in docDictionary:
                resultDocIDlist.append(docID)
                documentWeights[docID] += self.rRController.invertedIndex[term][docID][0] * queryDictionary[term]

        for term in self.rRController.invertedIndex:
            if queryDictionary.get(term, None) is None:
                docDictionary = self.rRController.getDocIDsFromTerm(term)
                for docID in docDictionary:
                    resultDocIDlist.append(docID)
                    if documentWeights.get(docID, None) is None:
                        documentWeights[docID] = 0

        if self.automated is True and self.randomOrder is True:
                self.collectShuffledResults(documentWeights)
        elif self.automated is True and self.randomOrder is False:
            self.collectOrderedResults(documentWeights)
        else:
            self.printOrderedResults(documentWeights)

    def collectOrderedResults(self, finalResult):
        orderedTupples = sorted(finalResult.items(), key=operator.itemgetter(1))
        orderedTupples.reverse()

        itemInfoIndex = defaultdict(float)
        itemInfoType  = defaultdict()
        for id in orderedTupples:
            item = self.database.getItemByID(id[0])
            result = self.database.getInfoByID(id[0])
            itemInfoIndex[item]+=id[1]
            itemInfoType[item] = result[0][2]

        i = 1
        truePositiveList = list()
        for id in orderedTupples:
            result = self.database.getInfoByID(id[0])
            url = result[0][0]
            title = result[0][1]
            type = result[0][2]
            name = self.database.getItemByID(id[0])
            weight = str(id[1])
            itemID = self.database.getIDByNameType(self.currentQuery,type)
            if itemID is None:
                itemID = 0
            truePositiveList.append(self.database.checkIfRelevant(int(id[0]),itemID))
            i+=1
        self.evaluator.setActiveList(truePositiveList)
        self.evaluator.precessionAtK(10)
        self.evaluator.precessionAtR()
        self.evaluator.averagePrecession()
        self.evaluator.areaUnderTheCurve()

    def collectShuffledResults(self, finalResult):
        orderedTupples = sorted(finalResult.items(), key=operator.itemgetter(1))
        orderedTupples.reverse()

        itemInfoIndex = defaultdict(float)
        itemInfoType  = defaultdict()
        for id in orderedTupples:
            item = self.database.getItemByID(id[0])
            result = self.database.getInfoByID(id[0])
            itemInfoIndex[item]+=id[1]
            itemInfoType[item] = result[0][2]

        i = 1
        truePositiveList = list()
        random.shuffle(orderedTupples)
        for id in orderedTupples:
            #if i == 4:
            #    break
            result = self.database.getInfoByID(id[0])
            url = result[0][0]
            title = result[0][1]
            type = result[0][2]
            name = self.database.getItemByID(id[0])
            weight = str(id[1])
            itemID = self.database.getIDByNameType(self.currentQuery,type)
            if itemID is None:
                itemID = 0
            truePositiveList.append(self.database.checkIfRelevant(int(id[0]),itemID))
            i+=1
        random.shuffle(truePositiveList)
        self.evaluator.setActiveList(truePositiveList)
        self.evaluator.precessionAtK(10)
        self.evaluator.precessionAtR()
        self.evaluator.averagePrecession()
        self.evaluator.areaUnderTheCurve()


    def printOrderedResults(self, finalResult):
        orderedTupples = sorted(finalResult.items(), key=operator.itemgetter(1))
        orderedTupples.reverse()

        print("\nItem Search Results:")

        itemInfoIndex = defaultdict(float)
        itemInfoType  = defaultdict()
        for id in orderedTupples:
            item = self.database.getItemByID(id[0])
            result = self.database.getInfoByID(id[0])
            itemInfoIndex[item]+=id[1]
            itemInfoType[item] = result[0][2]
        sortedItemInfoIndexTuple = sorted(itemInfoIndex.items(), key=operator.itemgetter(1))
        sortedItemInfoIndexTuple.reverse()
        i=1
        for item in sortedItemInfoIndexTuple:
            if i == 4:
                break
            itemName = item[0]
            print(itemInfoType[itemName] + ": " + itemName + " (" + str(itemInfoIndex[itemName]) + ")")
            i+=1

        print("\n")
        i = 1
        for id in orderedTupples:
            #if i == 4:
            #    break
            result = self.database.getInfoByID(id[0])
            url = result[0][0]
            title = result[0][1]
            type = result[0][2]
            name = self.database.getItemByID(id[0])
            weight = str(id[1])
            itemID = self.database.getIDByNameType(self.currentQuery,type)
            if itemID is None:
                itemID = 0
            print(str(i) + ".\t" + title + "\t(" + weight + ")\n\t" + url + "\n\t" + type + ": " + name + "\tRelevant: "+str(self.database.checkIfRelevant(int(id[0]),itemID))+"\n")
            i+=1
        print("Results in Corpus: "+str(i))
