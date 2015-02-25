__author__ = 'Jordan Smith'

import sqlite3
import re
import os
from collections import defaultdict

class WebDB(object):

    def __init__(self, dbfile):
        """
        Connect to the database specified by dbfile.  Assumes that this
        dbfile already contains the tables specified by the schema.
        """
        self.dbfile = dbfile
        self.cxn = sqlite3.connect(dbfile)
        self.cur = self.cxn.cursor()


        self.execute("""CREATE TABLE IF NOT EXISTS CachedURL (
                                 id  INTEGER PRIMARY KEY,
                                 url VARCHAR,
                                 title VARCHAR,
                                 docType VARCHAR
                            );""")

        self.execute("""CREATE TABLE IF NOT EXISTS URLToItem (
                                 id  INTEGER PRIMARY KEY,
                                 urlID INTEGER,
                                 itemID INTEGER
                            );""")

        self.execute("""CREATE TABLE IF NOT EXISTS Item (
                                 id  INTEGER PRIMARY KEY,
                                 name VARCHAR,
                                 type VARCHAR
                            );""")



    def _quote(self, text):
        """
        Properly adjusts quotation marks for insertion into the database.
        """

        text = re.sub("'", "''", text)
        return text

    def _unquote(self, text):
        """
        Properly adjusts quotations marks for extraction from the database.
        """

        text = re.sub("''", "'", text)
        return text


    def execute(self, sql):
        """
        Execute an arbitrary SQL command on the underlying database.
        """
        res = self.cur.execute(sql)
        self.cxn.commit()

        return res


    ####----------####
    #### CachedURL ####

    def lookupCachedURL_byURL(self, url):
        """
        Returns the id of the row matching url in CachedURL.
        If there is no matching url, returns an None.
        """
        sql = "SELECT id FROM CachedURL WHERE URL='%s'" % (self._quote(url))
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        elif len(reslist) > 1:
            raise RuntimeError('DB: constraint failure on CachedURL.')
        else:
            return reslist[0][0]


    def lookupCachedURL_byID(self, cache_url_id):
        """
        Returns a (url, docType, title) tuple for the row
        matching cache_url_id in CachedURL.
        If there is no matching cache_url_id, returns an None.
        """
        sql = "SELECT url, docType, title FROM CachedURL WHERE id=%d"\
              % (cache_url_id)
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist[0]


    def lookupItem(self, name, itemType):
        """
        Returns a Item ID for the row
        matching name and itemType in the Item table.
        If there is no match, returns an None.
        """
        print(name)
        sql = "SELECT id FROM Item WHERE name='%s' AND type='%s'"\
            % (self._quote(name), self._quote(itemType))
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist[0][0]

    def lookupURLToItem(self, urlID, itemID):
        """
        Returns a urlToItem.id for the row
        matching name and itemType in the Item table.
        If there is no match, returns an None.
        """
        sql = "SELECT id FROM UrlToItem WHERE urlID=%d AND itemID=%d"\
              % (urlID, itemID)
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            return reslist[0]

    def deleteCachedURL_byID(self, cache_url_id):
        """
        Delete a CachedURL row by specifying the cache_url_id.
        Returns the previously associated URL if the integer ID was in
        the database; returns None otherwise.
        """
        result = self.lookupCachedURL_byID(cache_url_id)
        if result == None:
            return None

        (url, download_time, docType) = result

        sql = "DELETE FROM CachedURL WHERE id=%d" % (cache_url_id)
        self.execute(sql)
        return self._unquote(url)



    def insertCachedURL(self, url, docType=None, title=None):
        """
        Inserts a url into the CachedURL table, returning the id of the
        row.

        Enforces the constraint that url is unique.
        """
        if docType is None:
            docType = ""

        cache_url_id = self.lookupCachedURL_byURL(url)
        if cache_url_id is not None:
            return cache_url_id

        sql = """INSERT INTO CachedURL (url, docType, title)
                 VALUES ('%s', '%s','%s')""" % (self._quote(url), docType, title)

        res = self.execute(sql)
        return self.cur.lastrowid


    def insertItem(self, name, itemType):
        """
        Inserts a item into the Item table, returning the id of the
        row.
        itemType should be something like "music", "book", "movie"

        Enforces the constraint that name is unique.
        """


        item_id = self.lookupItem(name, itemType)
        if item_id is not None:
            return item_id

        sql = """INSERT INTO Item (name, type) VALUES ('%s', '%s')""" % (self._quote(name), self._quote(itemType))

        res = self.execute(sql)
        return self.cur.lastrowid

    def getInfoByID(self, urlID):
        """
        :param itemID:
        :return tuple(urlTitle, URL, itemType:
        """

        sql = "SELECT url, title, docType FROM CachedURL WHERE id='%s'" % (urlID)
        res = self.execute(sql)
        reslist = res.fetchall()
        return reslist

    def getItemByID(self, urlID):
        """
        :param itemID:
        :return tuple(itemTitle, itemType:
        """
        sql = "SELECT itemID FROM URLToItem WHERE urlID=%s" % (urlID)
        res = self.execute(sql)
        reslist = res.fetchall()
        if reslist == []:
            return None
        else:
            sql = "SELECT name FROM Item where id=%s" % reslist[0][0]
            res = self.execute(sql)
            reslist = res.fetchall()
            if reslist == []:
                return None
            else:
                return reslist[0][0]

    def insertURLToItem(self, urlID, itemID):
        """
        Inserts a item into the URLToItem table, returning the id of the
        row.
        Enforces the constraint that (urlID,itemID) is unique.
        """


        u2i_id = self.lookupURLToItem(urlID, itemID)
        if u2i_id is not None:
            return u2i_id

        sql = """INSERT INTO URLToItem (urlID, itemID)
                 VALUES ('%s', '%s')""" % (urlID, itemID)

        res = self.execute(sql)
        return self.cur.lastrowid

    def getIDFromURL(self, theURL):
        """
        :param theURL:
        :return tuple(urlTitle, URL, itemType:
        """

        sql = "SELECT id FROM CachedURL WHERE id='%s'" % (theURL)
        res = self.execute(sql)
        reslist = res.fetchall()
        return reslist


class Wrapper(object):

    def __init__(self):
        if not os.path.exists("data/"):
            os.path.mkdir("data/")
        if not os.path.exists("data/clean/"):
            os.path.mkdir("data/clean/")
        if not os.path.exists("data/header/"):
            os.path.mkdir("data/header/")
        if not os.path.exists("data/raw/"):
            os.path.mkdir("data/raw/")
        if not os.path.exists("data/cache"):
            os.path.mkdir("data/cache")

    def createCleanFile(self, input, id):
        filename = self.getFileNameFromID(id)
        fo = open(("data/clean/" + filename), "w+")

        #if (type(dict) == type(defaultdict())):
        #    for key, value in dict.items():
        #        fo.write(str(key) + "\n")

        fo.write(input)
        fo.close()

    def createRawFile(self, input, id):
        filename = self.getFileNameFromID(id)
        fo = open(("data/raw/" + filename), "w+")

        fo.write(input)
        fo.close()

    def createHeaderFile(self, input, id):
        filename = self.getFileNameFromID(id)
        fo = open(("data/header/" + filename), "w+")

        fo.write(input)
        fo.close()

    def getFileNameFromID(self, id):
        filename = "" + str(id)
        while (len(filename) <= 6):
            filename = "0" + filename

        return filename + ".txt"
