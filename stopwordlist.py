# author: Kumar Prasad Dahal
# 2/7/2017
# Stop words are most frequent terms occuring in documents like the, an, of, as, in etc. 
# This program generates the stop words list that is used during stop words removal phase.

import sys
import os
import re

fileDir = os.path.dirname(os.path.realpath('__file__'))
stopwordfile = "stopwords.txt"
stopwords=[]
def findStopWords():
    try:
        inputfile = open(stopwordfile,'r')
        lines = inputfile.readlines()
        for line in lines:
            stopwords.extend(re.findall('[a-zA-Z]+',line.lower().strip()))
        inputfile.close()
        return set(stopwords)
        
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception:
        exception = sys.exc_info()[0]
        print("Error: ",exception)
      
#print(findStopWords())


