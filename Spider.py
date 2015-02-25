__author__ = 'andrew'

import HTMLGetter
import SoupMachine
from collections import defaultdict
import nltk
import nltk.data
import re
from nltk.stem import *
import Database
import time
import random

class Spider():
    html        = None
    soupMachine = None
    mlStriper   = None
    htmlGetter  = None
    database    = None

    def __init__(self):
        self.htmlGetter = HTMLGetter.HTMLGetter()
        self.database = Database.WebDB("data/cache/database.db")


    def fetch(self, url, doctype, item):
        # check if entry already exists
        id = self.database.lookupCachedURL_byURL(url)
        if id is not None:
            return id
        # take a short break
        time.sleep(random.uniform(3, 6))
        html = self.htmlGetter.getHTMLFromURL2(url)
        self.soupMachine = SoupMachine.SoupMachine(html)
        title = self.soupMachine.getTitle()

        title = title.replace("'", "")
        header = self.htmlGetter.getHeader()
        htmlPageString = str(html)

        id = self.database.insertCachedURL(url, doctype, title)
        itemID = self.database.insertItem(item, doctype)
        self.database.insertURLToItem(id, itemID)


        #Finish tokenization
        self.soupMachine.removeJunk()
        strippedhtml = self.removePunc(self.removeComments(self.removeHtmlComments(self.soupMachine.getText())))
        lowercaseTokenList = self.removeUpperFromObject(nltk.word_tokenize(strippedhtml))
        terms = self.convertListToDictionary(lowercaseTokenList)

        lowercaseTokenString = '\n'.join(lowercaseTokenList)
        #Create all text files.
        databaseWrapper = Database.Wrapper()

        databaseWrapper.createCleanFile(lowercaseTokenString, id)
        databaseWrapper.createRawFile(htmlPageString, id)
        databaseWrapper.createHeaderFile(header, id)


        return id

    def removeComments(self, string):
        string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
        return string

    def removeHtmlComments(self, string):
        string = re.sub(re.compile("<!--.*?-->",re.DOTALL ) ,"" ,string) # remove all occurance HTML comments (<!-- -->) from string
        return string

    def removePunc(self, string):
        string = re.sub(re.compile("[^-.\"'\w\s]",re.DOTALL ) ,"" ,string) # remove all occurances punctuation
        return string

    def removeUpperFromObject(self, objects):
        for i in range(len(objects)):
            objects[i] = objects[i].lower()

        return objects

    def convertListToDictionary(self, list):
        dictionary = defaultdict(int)
        for token in list:
            dictionary[token] += 1
        return dictionary

    def convertToPorterTerms(self, terms):
        porterTerms = []
        for i in terms:
            porterTerms.append(PorterStemmer().stem_word(i))
        return porterTerms