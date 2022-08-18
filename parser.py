#!/usr/bin/python

import os
import json
import re
from pyquery import PyQuery as pq

'''
NOTE: please use 3 folders of raw htmls from here:
https://drive.google.com/drive/folders/1NNlh6XBIVETbLmqu2kw9yfJ_GvaLfGH9?usp=sharing
'''

# files
JSONFILE = 'bible.json'
# IMPORTANT! When exporting to Chrome and saving to PDF,
# User margin = 0.35" (left-right) and 0.7 (top-bottom)
BOOKTOPRINT = 'Genesis' 


# get rid of tags
CLEANR = re.compile('<.*?>') 
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext.strip()

# create html file => to print to pdf, use Chrome + scale=90%
def createlinearfile():
    with open(JSONFILE, 'r') as f:
        obj = json.load(f)
    bookCount = len(obj)
    out = '<html><body><div style="margin: 40px;">'

    # better print one book at a time or break the computer
    bookName = BOOKTOPRINT
    out += "<h3>%s</h3>"%bookName
    for k, v in obj.items():
        if v['book'] == bookName:
            verses = v['verses']
    for k, v in verses.items():
        print(v)
        out += "<span><b>%s</b></span><br/>"%k
        out += '<span>&#8688; %s</span><br/>'%v['eng']
        out += '<span>&#8688; %s</span><br/>'%v['deu']
        out += '<span>&#8688; %s</span><br>'%v['fr']
    out += "</div></body></html>"
    with open('out.html', 'w', encoding='utf-8') as f:
        f.write(out)
# create html file => to print to pdf, use Chrome + scale=90%
def createtablefile():
    with open(JSONFILE, 'r') as f:
        obj = json.load(f)
    bookCount = len(obj)
    out = '<html><body><div style="margin: 30px;">'

   # better print one book at a time or break the computer
    bookName = BOOKTOPRINT
    out += "<h3>%s</h3>"%bookName
    for k, v in obj.items():
        if v['book'] == bookName:
            verses = v['verses']
    out += '<table style="width:100%;table-layout:fixed;border-spacing:9px;">'
    for k, v in verses.items():
        out += '<tr><td>%s</td>'%v['eng']
        out += '<td>%s</td>'%v['deu']
        out += '<td>%s</td></tr>'%v['fr']
    out += "</table></div></body></html>"
    with open('%s.html'%BOOKTOPRINT, 'w', encoding='utf-8') as f:
        f.write(out)

def generatemap():
    eng_folder = "/Users/salisal./bible/kj_new/"
    deu_folder = "/Users/salisal./bible/de_new/"
    fr_folder = "/Users/salisal./bible/fr_new/"

    # specify folders & encoding schemes
    folders = [eng_folder, deu_folder, fr_folder]
    encodings = ['iso-8859-15','utf-8','utf-8-sig']

    output = {}
    for i in range(1,67):
        padded_i = str(i).zfill(2) # padded for subfolder name
        output[i] = {}
        verseEntry = {}
        for j in range(0,3):
            encoding = encodings[j]
            files = os.listdir(folders[j]+padded_i)
            fileCount = len(files)
            for k in range(1, fileCount+1):
                fileNo = k
                fullFileName = folders[j]+padded_i+'/'+str(fileNo)+'.htm'
                print(fullFileName + " - " + str(fileNo))
                with open(fullFileName, "r", encoding=encoding, errors="ignore") as f:
                    contents = f.read()
                    doc = pq(contents)
                    book = doc("h1").text()
                    if j == 0: # take book name from English only
                        output[i]["book"] = book 
                    print('*** '+book)
                    section = doc("h3").text()
                    verses = doc(".textBody").text().split('\n')
                   
                    for verse in verses:
                        language = "eng" if j == 0 else ("deu" if j == 1 else "fr")
                        if not verse[0].isdigit(): # e.g. Chapter xx
                            continue
                        no = verse[0:3].strip() if verse[0:3].isdigit() else (verse[0:2].strip() if verse[0:2].isdigit() else verse[0:1])
                        verseNo = str(k)+"-"+no
                        verseText = verse[3:].strip() if verse[0:3].isdigit() else (verse[2:].strip() if verse[0:2].isdigit() else (verse[1:].strip() if verse[0:1].isdigit() else verse))

                        if verseNo not in verseEntry:
                            verseEntry[verseNo] = {}
                        verseEntry[verseNo][language] = verseText
                        
        output[i]["verses"] = verseEntry

    with open(JSONFILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

createtablefile()
