__author__ = 'andrew'
import urllib.request
import time
import socket

class HTMLGetter():

    reponse = None
    header = None
    mod = None
    pageText = None

    def getHTMLFromURL(self, url):
        try:
            self.response = urllib.request.urlopen(url)
            the_page = self.response.read()
            text = the_page.decode("iso-8859-1")
            return text
        except urllib.error.HTTPError as err:
            print(err)
            time.sleep(2)
            return self.getHTMLFromURL(url)

    def getHTMLFromURL2(self, url):
        try:
            u = urllib.request.URLopener() # Python 3: urllib.request.URLOpener
            u.addheaders = []
            u.addheader('User-Agent', 'Opera/9.80 (Windows NT 6.1; WOW64; U; de) Presto/2.10.289 Version/12.01')
            u.addheader('Accept-Language', 'de-DE,de;q=0.9,en;q=0.8')
            u.addheader('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1')
            f = u.open(url)
            thePage = f.read()
            self.header=f.info()
            if f.info()['Last-Modified']:
                self.mod=f.info()['Last-Modified']
            self.pageText=thePage.decode("iso-8859-1")
            f.close()
            return self.pageText
        except (urllib.error.HTTPError):
            import sys; ty, err, tb = sys.exc_info()
            print("HTTP Error: " + str(urllib.error.HTTPError))
            time.sleep(3)
            return "could not fetch URL"
        except socket.error:
            import sys; ty, err, tb = sys.exc_info()
            print("Socket Error.")
            time.sleep(3)
            return "socket error for URL"

    def getHeader(self):
            return str(self.header)