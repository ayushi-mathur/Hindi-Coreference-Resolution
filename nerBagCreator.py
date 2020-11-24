# Will create a file with a list of NE categories from nerData

import re

def folderWalk(folderPath):
    import os
    fileList = []
    for dirPath , dirNames , fileNames in os.walk(folderPath) :
        for fileName in fileNames :
            fileList.append(os.path.join(dirPath , fileName))
    return fileList

fl = folderWalk('./nerData')

ne_categories = []

for rfp in fl:
    inFile = open(rfp, 'r')
    for node in inFile.readlines():
        word = re.findall(r"af='([^,]*),", node)
        ne_category = re.findall(r"enamex_type='([^']*)'", node)
        if len(word) and len(ne_category):
            print(word[0], ne_category[0])
            if ne_category not in ne_categories:
                ne_categories.append(ne_category)

print(ne_categories)