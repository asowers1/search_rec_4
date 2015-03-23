__author__ = 'andrew'


class Evaluation:

    activeList = list()
    numberOfQueries = 0
    precisionAtK = 0.0
    precisionAtR = 0.0
    meanAveragePercision = 0.0
    AUC = 0.0

    def setActiveList(self, list):
        self.activeList = list
        self.numberOfQueries += 1

    def getTruesFromList(self):
        i = 0
        for item in self.activeList:
            if item == True:
                i+=1
        return i
    def getFalseFromList(self):
        i = 0
        for item in self.activeList:
            if item == False:
                i+=1
        return i

    def precessionAtK(self, K):
        trueRatio = 0.0
        i = 0
        for item in self.activeList:
            if i == K:
                self.precisionAtK += (trueRatio/K)
                return trueRatio/K
            if item == True:
                trueRatio+=1
            i+=1

    def precessionAtR(self):
        K = self.getTruesFromList()
        trueRatio = 0.0
        i = 0
        for item in self.activeList:
            if i == K:
                self.precisionAtR += (trueRatio/K)
                return trueRatio/K
            if item == True:
                trueRatio+=1
            i+=1

    def averagePrecession(self):
        average = 0
        trues = 0
        i = 1
        for item in self.activeList:
            if item == True:
                trues += 1
                average += trues/i

            i += 1

        self.meanAveragePercision += (average/trues)
        return average/trues

    def areaUnderTheCurve(self):
        trues = 0
        falses = 0
        trueCount = self.getTruesFromList()
        falseCount = self.getFalseFromList()

        areaUnderTheCurve = 0.0

        i = 0
        for item in self.activeList:
            if item == True:
                trues += 1
            else:
                falses += 1
                areaUnderTheCurve += (trues/trueCount) * (1/falseCount)
        i += 1

        self.AUC += areaUnderTheCurve
        return areaUnderTheCurve

    def printFinalAdverages(self):
        self.precisionAtK = self.precisionAtK/self.numberOfQueries
        self.precisionAtR = self.precisionAtR/self.numberOfQueries
        self.meanAveragePercision = self.meanAveragePercision/self.numberOfQueries
        self.AUC = self.AUC/self.numberOfQueries

        print("P@10: "+str(self.precisionAtK)+" P@R: "+str(self.precisionAtR)+ " MAP: "+str(self.meanAveragePercision)+" AUC: "+str(self.AUC))