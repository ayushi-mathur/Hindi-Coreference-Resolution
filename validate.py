import scripts.ssfapi.ssfAPI_intra as ssf

fileList = ssf.folderWalk('./data/')

validFiles = 0
totalFiles = 0

probFiles = []

for filepath in fileList:
    totalFiles += 1
    try:
        doc = ssf.Document(filepath)
        validFiles += 1

    except Exception as e:
        probFiles.append(filepath)
        continue

print("Total Valid Files : ", validFiles , "Out of", totalFiles)
print ("Invalid Files :")
for i in probFiles:
    print(i)