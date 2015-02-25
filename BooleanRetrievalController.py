__author__ = 'andrew'

import InvertedIndexModel
import Database
import math
from collections import defaultdict

class BooleanRetrievalController:

    invertedIndex = None
    database      = None

    def __init__(self):
        #setup Inverted Index Model
        self.invertedIndex = InvertedIndexModel.InvertedIndexModel()
        self.database = Database.WebDB("data/cache/database.db")
        return

    # takes in a query type, calls query method accordingly
    def queryIngest(self, queryType):
        if(queryType == "1"):
            self.singleTokenQuery()
        elif(queryType == "2"):
            self.andQuery()
        elif(queryType == "3"):
            self.orQuery()
        elif(queryType == "4"):
            self.phraseQuery()
        elif(queryType == "5"):
            self.nearQuery()

    # performs single token query
    def singleTokenQuery(self):
        query = input("Please enter a single word: ")
        i = 1
        finalResult = defaultdict(int)
        for key in self.invertedIndex.invertedIndex[query]:
            result = self.database.getInfoByID(key)
            url = result[0][0]
            title = result[0][1]
            type = result[0][2]
            name = self.database.getItemByID(key)

            finalResult[name] += 1
            print(str(i) + ".\t" + title + "\n\t" + url + "\n\t" + type + ": " + name + "\n")
            i += 1

        self.printCountResults(finalResult, i)

    # performs AND query
    def andQuery(self):
        query1 = input("Please enter first word: ")
        query2 = input("Please enter second word: ")
        i = 1
        dict1 = self.invertedIndex.invertedIndex[query1]
        dict2 = self.invertedIndex.invertedIndex[query2]
        list3 = set(dict1) & set(dict2)
        finalResult = defaultdict(int)
        for key in list3:
            result = self.database.getInfoByID(key)
            url = result[0][0]
            title = result[0][1]
            type = result[0][2]
            name = self.database.getItemByID(key)

            finalResult[name] += 1
            print(str(i) + ".\t" + title + "\n\t" + url + "\n\t" + type + ": " + name + "\n")
            i += 1

        self.printCountResults(finalResult, i)


    # performs OR query (essentially two single token queries)
    def orQuery(self):
        query1 = input("Please enter first word: ")
        query2 = input("Please enter second word: ")

        i = 1
        finalResult = defaultdict(int)

        # results from query one, iterate over data model
        for key in self.invertedIndex.invertedIndex[query1]:
            result = self.database.getInfoByID(key)
            url = result[0][0]
            title = result[0][1]
            type = result[0][2]
            name = self.database.getItemByID(key)

            finalResult[name] += 1
            print(str(i) + ".\t" + title + "\n\t" + url + "\n\t" + type + ": " + name + "\n")
            i += 1

        # results from query two, iterate over data model
        for key in self.invertedIndex.invertedIndex[query2]:
            result = self.database.getInfoByID(key)
            url = result[0][0]
            title = result[0][1]
            type = result[0][2]
            name = self.database.getItemByID(key)

            finalResult[name] += 1
            print(str(i) + ".\t" + title + "\n\t" + url + "\n\t" + type + ": " + name + "\n")
            i += 1

        # print results
        self.printCountResults(finalResult, i)

    # performs phrase query
    def phraseQuery(self):

        query1 = input("Please enter first word: ")
        query2 = input("Please enter second word: ")

        dict1 = self.invertedIndex.invertedIndex[query1]
        dict2 = self.invertedIndex.invertedIndex[query2]
        list3 = list(set(dict1) & set(dict2))
        finalResult = defaultdict(int)
        i = 1
        for item in list3:
            for dict1Elements in dict1[item]:
                for dict2Elements in dict2[item]:
                    if dict1Elements+1 == dict2Elements:
                        result = self.database.getInfoByID(item)
                        url = result[0][0]
                        title = result[0][1]
                        type = result[0][2]
                        name = self.database.getItemByID(item)
                        finalResult[name] += 1
                        print(str(i) + ".\t" + title + "\n\t" + url + "\n\t" + type + ": " + name + "\n")
                        i = i+1

        self.printCountResults(finalResult,i)


    # performs near query
    def nearQuery(self):
        query1 = input("Please enter first word: ")
        query2 = input("Please enter second word: ")

        dict1 = self.invertedIndex.invertedIndex[query1]
        dict2 = self.invertedIndex.invertedIndex[query2]
        list3 = list(set(dict1) & set(dict2))
        finalResult = defaultdict(int)
        i = 1
        for item in list3:
            for dict1Elements in dict1[item]:
                for dict2Elements in dict2[item]:
                    difference = math.fabs(dict1Elements - dict2Elements)
                    if difference <= 5:
                        result = self.database.getInfoByID(item)
                        url = result[0][0]
                        title = result[0][1]
                        type = result[0][2]
                        name = self.database.getItemByID(item)
                        finalResult[name] += 1
                        print(str(i) + ".\t" + title + "\n\t" + url + "\n\t" + type + ": " + name + "\n")
                        i = i+1

        # print results
        self.printCountResults(finalResult, i)

    # helper function to print results to console
    def printCountResults(self, finalResult, total):
        print("total: " + str(total-1))
        highestValue = 0
        highestKey = ''
        for item in finalResult:
            if finalResult[item] > highestValue:
                highestValue = finalResult[item]
                highestKey = item

        print(highestKey + " ("+str(highestValue)+")")