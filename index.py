#!C:\Python34\python.exe

# author: Kumar Dahal
# 2/7/2017
# This program provides GUI interface to send user query

import cgi
import retrivedocuments
global invertedindexmatrix
import invertedindex
import stopwordlist
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
stopwords= stopwordlist.findStopWords()
invertedindexmatrix =(invertedindex.invertedIndex(fileDir+ "/Files-Output/"))
print ("Content-type:text/html\r\n\r\n")

form = cgi.FieldStorage() 

print("<form action='index.py' method='post'>")
print("<div style=\"margin-left:50;margin-right:auto;margin-top:50;width:600;float:left;align=left\">")
print("<p style=\"font-size:16;\"><strong>Query:</strong>  <input type=text name='query'>&nbsp;&nbsp;<input type=submit name='btnSearch' value=\"Search\"></p>")	

if form.getvalue('btnSearch'):
	if form.getvalue('query'):
		userquery=form.getvalue('query')
		retrivedocuments.retriveWebPages(userquery,invertedindexmatrix,stopwords)

print("</div>")
print("</form>")
