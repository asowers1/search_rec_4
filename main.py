__author__ = 'andrew'
import Spider
from google import search
import random
import BooleanRetrievalController
import rankedRetrivalController

def buildDataSet():

    books = open("data/item/book.txt", "r")
    bookList = []
    for book in books:
        bookList.append(book.rstrip())

    movies = open("data/item/movie.txt", "r")
    movieList = []
    for movie in movies:
        movieList.append(movie.rstrip())

    songs = open("data/item/music.txt", "r")
    songList = []
    for song in songs:
        songList.append(song.rstrip())

    spider = Spider.Spider()

    for item in bookList:
        urls = search(item + " book", 'com', 'en', '0', 'off', 1, 0, 11, random.uniform(15.0, 45.0), True, {}, '')
        for url in urls:
            if(type(url) is str):
                print(spider.fetch(url, "book", item))

    for item in movieList:
        for url in search(item + " movie", 'com', 'en', '0', 'off', 1, 0, 11, random.uniform(15.0, 45.0), True, {}, ''):
            if type(url) is str:
                print(spider.fetch(url, "movie", item))


    for item in songList:
        for url in search(item + " song", 'com', 'en', '0', 'off', 1, 0, 11, random.uniform(15.0, 45.0), True, {}, ''):
            if type(url) is str:
                print(spider.fetch(url, "song", item))

    books.close()
    movies.close()
    songs.close()

def BR():
    booleanRetrivalController = BooleanRetrievalController.BooleanRetrievalController()
    status = True
    while status:
        print("Command Options\n\t1) Token query\n\t2) AND query\n\t3) OR query\n\t4) Phrase query\n\t5) Near query\n\t6) QUIT\n\n")
        option = input("Please type a number (1-6): ")
        if option == '6':
            status = False
            break
        booleanRetrivalController.queryIngest(option)

def RR():
    #wIIM = weightedInvertedIndexModel.weightedInvertedIndexModel()
    #wIIM.printInvertedIndex()
    #wIIM.printDocLength()
    rankedRetrivalController.rankedRetrivalController()
#buildDataSet()
#BR()

RR()