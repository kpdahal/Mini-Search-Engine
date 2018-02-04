# author: Kumar Dahal
# 2/7/2017
# This program retrives most relevant urls based on user query.
# In this step we perform calculations to find out similarities between user query and documents.
# 1) we calculate term frequency and inverse document frequency that is used to calculate the weight of each word.
# 2) we use this weight to find the cosine similarity between query and docs.
# 3) we sort the docs based on  cosine similarity score and present the relevent docs to user.

import re
import invertedindex
import stopwordlist
import os
import math
from nltk.stem import PorterStemmer
import collections
import sys

fileDir = os.path.dirname(os.path.realpath('__file__'))
stemmer = PorterStemmer()

#Find total number of documents in processed document directory
path = fileDir+ "/Files-Output/"
totaldocuments=len([docname for docname in os.listdir(path) if os.path.isfile(os.path.join(path, docname))])

invertedindexmatrix =(invertedindex.invertedIndex(path))[0]
termdocument = (invertedindex.invertedIndex(path))[1]
stopwords = stopwordlist.findStopWords()

def calculateDocumentLength():
    try:
        doclength=collections.defaultdict(dict)
        #sum square of occurence of each term in a file and store in a dictionary
        for file,termfreq in termdocument.items():
            lenfile=0
            for term, freq in termfreq.items():
                lenfile+= (freq*freq)
            doclength[file]=math.sqrt(lenfile)
        return doclength
        
    except FileNotFoundError:
        print("File is missing.")
    except Exception:
        exception = sys.exc_info()[0]
        print("Error: ",exception) 
        
        
def retriveWebPages(userquery,invertedindexmatrix,stopwords):
    try:
        #preprocessed the query first using same logic to preprocess documents
        words = re.findall('[a-zA-Z]+',userquery.lower().strip())
        preprocessed_querywords= [stemmer.stem(token) for token in words if token not in stopwords]

        score_documents={}
        for word in preprocessed_querywords:
            #start calculation if the word is in inverted index dictionary
            if word in invertedindexmatrix:
                weightquery=0
                lenquery=0
                qwordcount=preprocessed_querywords.count(word)
                #find no of documents that contain query word
                doc_qwords=len(invertedindexmatrix[word])
                
                #find inverse document frequery for query word
                idfword=math.log(totaldocuments/doc_qwords)
    
                # find TFIDF for query 
                weightquery = qwordcount *idfword
                
                #find query length
                lenquery+=weightquery*weightquery
                query_length = math.sqrt(lenquery)
    
                document_frequency=invertedindexmatrix[word]
                
                #calculate numerator score for cosine similarity
                for doc in document_frequency.keys():
                    weightdocument=0
                    qdoccount=document_frequency[doc]
                    #find TFIDF for document 
                    weightdocument=(idfword * qdoccount)
    
                    if doc not in score_documents:
                        score_documents[doc]=(weightquery *weightdocument)
                    else: 
                        score_documents[doc]+=(weightquery * weightdocument)

                    #Normalize the score by dividing weight by product of  length of document and length of query
                    document_length = calculateDocumentLength()
                    score_documents[doc]=(score_documents[doc]/(document_length[doc]*query_length))
     
        print("Following are the most relevant pages: "+ '<br>')
        for doc ,score in sorted(score_documents.items(), key=lambda item:-item[1]):
           file  = open("Files-Output/"+doc,'r')
           link = file.read().split("\n").pop(0)
           print('<a href="'+link+'" target="new">'+link+'</a>'+'<br>')
           file.close()
    except FileNotFoundError:
        print("Error: File not found.")
    except ZeroDivisionError:
        print("Error:Divide by Zero.")
    except Exception:
        exception = sys.exc_info()[0]
        print("Error: ",exception)
        
print(retriveWebPages("memphis",invertedindexmatrix,stopwords))
       

