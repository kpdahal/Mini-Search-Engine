# author: Kumar Dahal
# 2/7/2017
# This program generates the inverted index and term document dictionary.
# Each entry of the inverted index matrix represents the frequency of occurrances of that word on that file.
#Each entry of term document dictionary represent the word frequency of each word in each documents 

import os
import collections
import sys

fileDir = os.path.dirname(os.path.realpath('__file__'))

def invertedIndex(path):
    try:
        invertedindex= collections.defaultdict(dict)
        termdocument=collections.defaultdict(dict)
        
        filelist = os.listdir(path)
        for filename in filelist:
            file=open(path+filename,'r')
            lines= file.readlines()
            wordfrequency=collections.defaultdict(dict)
            for word in lines:
                word=word.lower().strip()
                #count word of each file and put it in a dictionary 
                if word in wordfrequency:
                    wordfrequency[word]+=1
                else:
                    wordfrequency[word]=1
                #create matrix of word and file
                invertedindex[word][filename]=wordfrequency[word]
                #create term document dictionary
                termdocument[filename]=wordfrequency
                
        return invertedindex, termdocument
    except FileNotFoundError:
        print("File is missing.")
    except Exception:
        exception = sys.exc_info()[0]
        print("Error: ",exception)
        
#print(invertedIndex(fileDir+ "/Files-Output/"))