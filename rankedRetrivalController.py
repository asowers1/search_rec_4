__author__ = 'andrew'
import weightedInvertedIndexModel
import Database
import math

class rankedRetrivalController:

    rRController = None
    database     = None
    smartVarientDoc = None
    smartVarientQuery = None

    def __init__(self):
        print("Supported SMART variants: [n,l][n,t][n,c] (default is 'ltc')\n")
        self.smartVarientDoc = input("Please enter SMART variant for documents:")
        self.smartVarientDoc = input("Please enter SMART variant for queries:")

        self.queryIngest()

    def queryIngest(self):
        if (self.smartVarientDoc == "ltc" and self.smartVarientQuery == "ltc"):
            self.ltc()

    def ltc(self):
        query = input("Enter Query or 'QUIT':")
        while query is not "QUIT":
            self.rRController = weightedInvertedIndexModel.weightedInvertedIndexModel()