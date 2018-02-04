# author Kumar Dahal
# 2/7/2017
# This program preprocessed the raw content collected by user  and outputs clean text
#  In prepprocessing phase:
# 1) text is converted to lower form and striped
# 2) url and email addresses are removed
# 3) punctuations are removed from each words
# 4) words are converted to its root word by stemming
# 5) removes stop words that are of no semantic significane. 

import os
import re
from nltk.stem import PorterStemmer
import sys
import stopwordlist

fileDir = os.path.dirname(os.path.realpath('__file__'))

#Use Porter Stemmer to handle morphological variation
stemmer = PorterStemmer()

def preProcessDocuments(path):
    try:
        filelist = os.listdir(path)
        stopwords = stopwordlist.findStopWords()
        #process each file on by one from file list
        for filename in filelist:
            inputfile=open(path+filename,'r')
            lines = inputfile.readlines()
            cleantokens = []
        
            for line in lines:
                #convert text to lower case
                line=line.lower().strip()
                #remove url from text
                line = re.sub(r'(https|http)?:\/\/([a-z0-9]+|\/|\.|\&||\?|\#)*', '', line )
                #remove email address from the text
                line = re.sub(r'[\w\-._$#*!%=?+]+@[\w\-._$#*!%=?+]*','',line)
                #remove punctuation and everything except words from text
                line = re.sub(r'[^\w]', ' ', line)
                #extract only character words from text
                cleantokens.extend(re.findall('[a-zA-Z]+',line))
            inputfile.close()
            
            outputfile = open("Files-Output/"+filename+"_processed"+".txt",'w')
            #create a list and store only those words that are not in stop words list
            filteredwords = [stemmer.stem(token) for token in cleantokens if token not in stopwords]
            
            for word in sorted(filteredwords):
                outputfile.write(word + " " + "\n")    
            outputfile.close()
        
        print("All files processed sucessfully.")
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception:
        exception = sys.exc_info()[0]
        print("Error: ",exception)
