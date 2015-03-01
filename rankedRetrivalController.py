__author__ = 'andrew'
import weightedInvertedIndexModel
import Database
import math

class rankedRetrivalController:

    rRController = None
    database     = None

    def __init__(self):
        self.rRController = weightedInvertedIndexModel.weightedInvertedIndexModel()
