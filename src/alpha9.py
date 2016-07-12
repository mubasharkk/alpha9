# @author : Mubashar Khokhar

import re
import string

import glob

import time
import datetime

from collections import Counter

class SearchEngine  (): 
    
    
    def __init__(self):
        self.booksList = []
        # Only loading :ISO-8859-1 encoded files
        self.booksList = self.getFilteredFiles()
#        self.booksList = glob.glob("books/*.txt")
        print '__init__';
        
    def getFilteredFiles(self):
        list = []
#        filesList = glob.glob("books/*.txt")
        filesList = glob.glob("sample/*.txt")
        
        for f in filesList:
            if not f.endswith("-8.txt") and not f.endswith("-0.txt"):
                list.append(f)
                
        return list
        
    # Can be scanned once and saved in a file or DBMS
    def scanLibrary (self):
        print 'scanning...', datetime.datetime.now()
        self.wordArray = []
        for book in self.booksList:
            self.wordArray += self.scanBook(book);
            
        self.wordArray = Counter(self.wordArray);
        print 'Library scanning completed!', datetime.datetime.now()

    """ Function complexity highly dependent on No. of files.
    For a larger set of files/data the memory will exhaust quickly
    """    
    def scanBook (self, bookPath):
        
        wordArray = [];
        lineArray = []     

        with open(bookPath) as f:
            for line in f:
                lineArray.append(line)

        for arr in lineArray:
            arr = re.sub('[^a-zA-Z\s]', '', arr).rstrip('\r\n')
            wordArray += arr.lower().split(' ')

        wordArray = Counter(wordArray)
        del wordArray[''];

    #    print wordArray.most_common(3);
        #print dict(wordArray)
        return wordArray


    def getCommonWords(self, num):        
        self.scanLibrary()
        return self.wordArray.most_common(num);
    
    def searchKeyword(self, word):
        print 'Searching for : ' , word,  'searching...';
        
        self.wordArray = []
        files = [];
        for book in self.booksList:
            self.wordArray = self.scanBook(book);
            if self.wordArray[word]:
                files.append((book, self.wordArray[word]))
        
        def getKey(item):
            return item[1]
        
        files = sorted(files, key = getKey, reverse = True)
        print 'Library searching completed!';
        
        return files
                



#search = SearchEngine()
#search.scanLibrary()
#print search.getCommonWords(20);
#
#print memory_usage.memory()
