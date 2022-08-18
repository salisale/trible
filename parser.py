#!/usr/bin/python

import os
import json
import re
import pdfkit
from pyquery import PyQuery as pq

'''
NOTE: please use 3 folders of raw htmls from here:
https://drive.google.com/drive/folders/1NNlh6XBIVETbLmqu2kw9yfJ_GvaLfGH9?usp=sharing
'''

# files
JSONFILE = 'bible.json'
IS_OUTPUT_JSON_MAP = True
IS_READ_FROM_JSON_MAP = True

def createHTMLString(jsonMap, bookName):
    out = '<html><body><div style="margin: 30px;">'

   # better create one book file at a time or break the computer
    out += "<h3>%s</h3>"%bookName
    for k, v in jsonMap.items():
        if v['book'] == bookName:
            verses = v['verses']
    out += '<table style="width:100%;table-layout:fixed;border-spacing:20px;">'
    for k, v in verses.items():
        out += '<tr><td>%s</td>'%v['eng'] if 'eng' in v else ''
        out += '<td>%s</td>'%v['deu'] if 'deu' in v else ''
        out += '<td>%s</td></tr>'%v['fr'] if 'fr' in v else ''
    out += "</table></div></body></html>"

    return out

def createPDFfile(bookName, htmlStr):
    def getConfig():
        return {
            'encoding': 'UTF-8',
            'page-size': 'A4',
            'margin-top': '0.7in',
            'margin-right': '0.35in',
            'margin-bottom': '0.7in',
            'margin-left': '0.35in'
        }
        
    pdfkit.from_string(htmlStr, bookName+".pdf", options = getConfig())


def generateMap():
    eng_folder = "/Users/salisal./bible/kj_new/"
    deu_folder = "/Users/salisal./bible/de_new/"
    fr_folder = "/Users/salisal./bible/fr_new/"

    # specify folders & encoding schemes
    folders = [eng_folder, deu_folder, fr_folder]
    encodings = ['iso-8859-15','utf-8','utf-8-sig']

    output = {}
    for i in range(1,67): # 66 folders or books
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
                    if j == 0: # take book name from English version only
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

    # output json file if configured
    if IS_OUTPUT_JSON_MAP:
        with open(JSONFILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

    return output

def run():
    if IS_READ_FROM_JSON_MAP:
        with open(JSONFILE, 'r') as f:
            obj = json.load(f)
    else:
        obj = generateMap()

    bookNames = [x['book'] for x in obj.values()]
    for book in bookNames:
        print('Generating %s ...'% book)
        htmlStr = createHTMLString(obj, book)
        createPDFfile(book, htmlStr)

run()
