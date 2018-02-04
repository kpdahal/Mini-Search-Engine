# author: Kumar Prasad Dahal 
# 2/7/2017
# This program crawls the web pages and save  preprocessed content on a output folder.

import re
import os
from bs4 import BeautifulSoup
import requests
from nltk.stem import PorterStemmer
import stopwordlist
import time


#Use relative path using os
fileDir = os.path.dirname(os.path.realpath('__file__'))
stopwords = stopwordlist.findStopWords()

#Use Porter Stemmer to handle morphological variation
stemmer = PorterStemmer()

starturl="http://www.memphis.edu/cs/"
url_list=[]
already_crawled=[]

def crawlWebPages(rooturl,numberofpages):
    
    try:
        cleanwords=[]
        print("Started reading: ",rooturl)
        rawurl  = requests.get(rooturl)
        rawdata = rawurl.text
        data = BeautifulSoup(rawdata,"lxml")
        text=data.get_text()
        #convert text to lower case
        text=text.lower().strip()
        #remove url from text
        text = re.sub(r'(https|http)?:\/\/([a-z0-9]+|\/|\.|\&||\?|\#)*', '', text )
        #remove email address from the text
        text = re.sub(r'[\w\-._$#*!%=?+]+@[\w\-._$#*!%=?+]*','',text)
        #remove punctuation and everything except word
        text = re.sub(r'[^\w]', ' ', text)
        #extract only character words from text
        cleanwords.extend(re.findall('[a-zA-Z]+',text)) 
        #restrict documents that contain less than 50 tokens
        if len(cleanwords)>50:
            docname=rooturl.split('//')[1].replace('/','_')
            file= "Files-Output/" + docname + ".txt"
            
            outputfile=open(file,'w')
            outputfile.write(rooturl + "\n" ) 
            #filter words using standard logic as followed in preprocessing documents
            filteredwords = [stemmer.stem(token) for token in cleanwords if token not in stopwords]
        
            for word in sorted(filteredwords):
                outputfile.write(word + " " + "\n")    
            outputfile.close()
        
        print("Completed reading: ",rooturl)
        
        #save already visted urls in a list and exclude those in next function call
        already_crawled.append(rooturl)
        for link in data.find_all('a',href=True):
            if(link.get('href').startswith('http') or link.get('href').startswith('https')):
                url_list.append(link.get('href').split('?')[0]) 
       
        for url in set(url_list):
            #exclude urls that link to pdf , word file, pictures and ppt file.
            #include only those urls that are of memphis.edu domain
            if not (url.endswith("pdf") or url.endswith("jpeg") or url.endswith("pptx") or url.endswith("docx")) and "memphis.edu" in url:
                if url not in already_crawled and ((len(already_crawled)<numberofpages)):
                    #pause for 3 seconds after every crawl
                    time.sleep(3)
                    print("Total pages crawled: ",len(already_crawled))
                    print("-------------------------------------------------------------------")
                    crawlWebPages(url,numberofpages)               
       
    except Exception as exception:
        print("An error occured while reading: ", rooturl," and the exception is: ",exception)
        print("-------------------------------------------------------------------")
        return []
#specify which is the starting url and how many numbers of pages you like to crawl while calling function
#print(crawlWebPages(starturl,1000))