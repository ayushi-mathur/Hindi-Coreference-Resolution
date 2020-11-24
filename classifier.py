import sys
sys.path
sys.path.append('./scripts/ssfapi/')
import ssfAPI_intra as ssf

from sklearn import tree

pronounsList = {'मैं', 'दैट', 'उसकी', 'उसके', 'जोकि', 'जहां', 'परस्पर', 'उसी', 'हमें', 'खुद', 'मेरा', 'यह', 'इससे', 'मुझे', 'इसे', 'इनसे', 'मुझ', 'इनको', 'कुछ', 'इस', 'सुपर', 'मेरी', 'उनमें', 'जो', 'जहाँ', 'तभी', 'तहां', 'जैसा', 'यही', 'दूसरे', 'यहीं', 'इसमें', 'ऐसी', 'ऐसा', 'आपकी', 'इसको', 'वहीं', 'इनकी', 'इनका', 'उन्हें', 'जिसमें', 'मैंने', 'आपको', 'इनके', 'जिसके', 'अपनी', 'अपना', 'वही', 'मैने', 'यहां', 'इसके', 'जिन्होंने', 'किसको', 'उनसे', 'जिसका', 'इसी', 'इसलिए', 'वहां', 'सभी', 'उसने', 'किसे', 'जिसने', 'उसे', 'उसका', 'आपका', 'इसकी', 'अपने', 'जिन्हें', 'NULL', 'यहाँ', 'इतना', 'आपके', 'उनका', 'कोई', 'मेरे', 'इसका', 'वो', 'कहीं', 'ऐसे', 'क्या', 'जिन', 'तब', 'कब', 'एक', 'किस', 'हमारी', 'दिस', 'किसने', 'जब', 'उनको', 'सब', 'इसने', 'जिससे', 'आप', 'आपस', 'हम', 'जिनमें', 'हमारे', 'कभी', 'जिनकी', 'इन', 'किन', 'इनमें', 'किसी', 'वे', 'स्वयं', 'अभी', 'उस', 'हमारा', 'हमने', 'इसीलिए', 'सबको', 'सबके', 'वह', 'वहाँ', 'उनकी', 'जिसको', 'तो', 'जिस', 'ये', 'इन्हीं', 'उन', 'अब', 'जिसकी', 'उन्होंने', 'इन्हें', 'हमसे', 'उनके', 'उससे', 'उसमें', 'जिसे'}

fl = ssf.folderWalk('./trainingdata')


trainingInput = []
trainingOutput = []
y = 0
w = 0
tp = 0
top = [0, 0, 0, 0, 0]

for rfp in fl:
    
    linearNodeList = []
    linearChunkList = []
    nodeFeatureList = []

    doc = ssf.Document(rfp)
    for s in doc.nodeList:
        for c in s.nodeList:
            linearChunkList.append(c)
    
    for i, c in enumerate(linearChunkList):
        for n in c.nodeList:
            if n.type in ['NN', 'NNP', 'NNPC', 'PRP'] and n.getAttribute('cref') is not None and (n.getAttribute('cref') != ''):
                temp = []
                for cref in n.getAttribute('cref').split(','):
                    temp.append(cref.split(':')[1])
                linearNodeList.append(temp)              
            else:
                linearNodeList.append([''])

            if (n.number == 'sg'):
                num = 1
            elif (n.number == 'pl'):
                num = 2
            else:
                num = 0

            if n.getAttribute('semprop') == 'h':
                anim = 1
            else: 
                anim = 0

            nodeFeatureList.append([num, i, int(c.upper.name) , 'NE', anim, n.morphPOS])
    
            if (n.type=='PRP') and (n.getAttribute('cref') is not None) and (n.getAttribute('cref') != ''):
                tp +=1
                for k, parsedNodes in enumerate(nodeFeatureList):
                    if (i - parsedNodes[1] < 1):
                        continue
                    
                    if (n.number == 'sg'):
                        num = 1
                    elif (n.number == 'pl'):
                        num = 2
                    else:
                        num = 0

                    if n.getAttribute('semprop') == 'h':
                        anim = 1
                    else: 
                        anim = 0
                    
                    trainingInput.append([num, parsedNodes[0], i - parsedNodes[1], int(c.upper.name) - parsedNodes[2]]) #,  parsedNodes[4], anim])
                    temp = []
                    for cref in n.getAttribute('cref').split(','):
                        temp.append(cref.split(':')[1])
                    if len(set.intersection(set(temp), set(linearNodeList[k]))):
                        trainingOutput.append(1)
                        y += 1
                    else:
                        trainingOutput.append(0)
                        w += 1

clf = tree.DecisionTreeClassifier()
clf = clf.fit(trainingInput, trainingOutput)

fl = ssf.folderWalk('./testingdata')

correct = 0
incorrect = 0


for rfp in fl:
    relfile = False
    doc = ssf.Document(rfp)

    linearChunkList = []
    linearNodeList = []
    nodeFeatureList = []
    j = -1
    for sentence in doc.nodeList:
        relsent = False
        for chunk in sentence.nodeList:
            j += 1
            linearChunkList.append(chunk)
            for node in chunk.nodeList:
                isPronoun = False
                
                if node.type in ['NN', 'NNP', 'NNPC', 'PRP'] and node.getAttribute('cref') is not None and (node.getAttribute('cref') != ''):
                    temp = []
                    for cref in node.getAttribute('cref').split(','):
                        temp.append(cref.split(':')[1])
                    linearNodeList.append(temp)              
                else:
                    linearNodeList.append([''])

                if (node.number == 'sg'):
                    num = 1
                elif (node.number == 'pl'):
                    num = 2
                else:
                    num = 0

                if node.getAttribute('semprop') == 'h':
                    anim = 1
                else: 
                    anim = 0

                nodeFeatureList.append([num, j, int(chunk.upper.name) , 'NE', anim, node.morphPOS])
                
                if (node.type=='PRP'):
                    
                    testingIO = []
                    goldOutput = []

                    mention = node
                    # ------------------------------------------------
                    for k, parsedNodes in enumerate(nodeFeatureList):
                        if (j - parsedNodes[1] < 1) and (j - parsedNodes[1] > 60):
                            continue
                        
                        if (node.number == 'sg'):
                            num = 1
                        elif (node.number == 'pl'):
                            num = 2
                        else:
                            num = 0

                        if node.getAttribute('semprop') == 'h':
                            anim = 1
                        else: 
                            anim = 0
                        
                        x = [num, parsedNodes[0], j - parsedNodes[1], int(chunk.upper.name) - parsedNodes[2]]  #,  parsedNodes[4], anim]
                        temp = []
                        if node.getAttribute('cref') is None:
                            goldOutput = 0
                        else:
                            for cref in node.getAttribute('cref').split(','):
                                temp.append(cref.split(':')[1])
                            if len(set.intersection(set(temp), set(linearNodeList[k]))):
                                goldOutput = 1
                            else:
                                goldOutput = 0
                        # print('tesIO before:', len(testingIO))                
                        testingIO.append([x, clf.predict_proba([x])[0], goldOutput])
                        # print('tesIO after:', len(testingIO))            

                    # print('tesIO:', len(testingIO))            
                    testingIO = sorted(testingIO, key= lambda y: y[1][1],reverse=True)
                    if testingIO[0][2] == 1 or testingIO[1][2] == 1 or testingIO[2][2] == 1 or testingIO[3][2] == 1 or testingIO[4][2] == 1:
                        correct += 1
                        # print('ding')
                    else:
                        incorrect += 1            
                                