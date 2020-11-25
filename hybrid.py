from sklearn import tree
import sys
sys.path
sys.path.append('./scripts/ssfapi/')
import ssfAPI_intra as ssf

import scripts.rulebased.relative as rv
import scripts.rulebased.reflexive as rx
import scripts.rulebased.locative as lt
import scripts.rulebased.thirdperson as tp
import scripts.rulebased.secondperson as sp
import scripts.rulebased.firstperson as fp

# ---------- CLASSIFIER TRAINING AREA -------------------

reflexivePronouns = ['अपनी', 'अपने', 'अपना', 'स्वयं', 'खुद', 'खुद']
relativePronouns = ['जो', 'जोकि', 'जहाँ', 'जिधर', 'जितना', 'जितने', 'जैसा', 'जैसे', 'जिसको', 'जिसके',
                    'जिस', 'जिसे', 'जिससे', 'जिसकी', 'जिसका', 'जिसने', 'जिन्हें', 'जिन्होंने', 'जिसमें', 'जिनमें', 'जिनकी']
firstPronouns = ['हमसे', 'हमारे', 'मेरा', 'मेरी', 'मेरे', 'हम', 'हमारा',
                 'हमने', 'मुझे', 'मैं', 'मुझ', 'मैने', 'हमें', 'मैंने', 'हमारी']
secondPronouns = ['आप', 'आपस', 'आपकी', 'आपके', 'आपको', 'आपका']
thirdPronouns = ['‌‌वह', 'वे', 'वो', 'उसको', 'उसने', 'उससे', 'उसका', 'उसकी', 'उसके', 'उन', 'उनको', 'उन्होंने', 'उनसे', 'उनका', 'उनकी', 'उनके']
locativePronouns = ['वहाँ', 'वहां', 'वहीं', 'यहीं', 'यहाँ',
                    'यहां', 'कहीं', 'इसमें', 'उसमें', 'इनमें']

pronounsList = reflexivePronouns + relativePronouns+firstPronouns+secondPronouns+thirdPronouns+locativePronouns

nerDict = {}
nerBag = open('nerBag', 'r')
for line in nerBag.readlines():
    nerDict[line.split(' ')[0]] = line.split(' ')[1].strip()

nerCategory = {
    'number': 1,
    'time': 2,
    'organization': 3,
    'location': 4,
    'person': 5,
    'measure': 6,
    'null': 0
}

fl = ssf.folderWalk('./trainingdata')

trainingInput = []
trainingOutput = []
y = 0
w = 0
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

            ne = nerDict.get(n.lex)
            if ne is not None:
                ne = nerCategory.get(ne)
            if ne is None:
                ne = 0

            nodeFeatureList.append(
                [num, i, int(c.upper.name), ne, anim, n.morphPOS])

            if (n.type == 'PRP') and (n.getAttribute('cref') is not None) and (n.getAttribute('cref') != ''):
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

                    trainingInput.append([num, parsedNodes[0], i - parsedNodes[1], int(
                        c.upper.name) - parsedNodes[2], parsedNodes[3], parsedNodes[4], anim])
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

# ---------- END OF CLASSIFIER TRAINING AREA -------------------


trainingfileList = ssf.folderWalk('./trainingdata/')
fileList = ssf.folderWalk('./testingdata/')

correct = 0
OOS = 0
incorrectWR = 0
incorrectClassifier = 0

unidentifiedNodes = [] # filename, sentence, chunk, name


for rfp in fileList:
    relfile = False

    doc = ssf.Document(rfp)
    linearChunkList = []
    linearNodeList = []
    nodeFeatureList = []

    j = -1

    for i, sentence in enumerate(doc.nodeList):
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

                ne = nerDict.get(node.lex)
                if ne is not None:
                    ne = nerCategory.get(ne)
                if ne is None:
                    ne = 0

                nodeFeatureList.append(
                    [num, j, int(chunk.upper.name), ne, anim, node.morphPOS])

                if node.lex in firstPronouns:
                    mention = node
                    answer = fp.firstperson(node)
                    isPronoun = True
                if node.lex in secondPronouns:
                    mention = node
                    answer = sp.secondperson(node)
                    isPronoun = True
                if node.lex in thirdPronouns:
                    mention = node
                    answer = tp.thirdperson(node, doc.nodeList[i-1] if i > 0 else None, doc.nodeList[i-2] if i > 1 else None, doc.nodeList[i-3] if i > 2 else None)
                    isPronoun = True
                if node.lex in reflexivePronouns:
                    mention = node
                    answer = rx.reflexive(
                        node, doc.nodeList[i-1] if i > 0 else None, doc.nodeList[i-2] if i > 1 else None)
                    isPronoun = True
                if (node.lex in relativePronouns) and (node.morphPOS == 'pn'):
                   mention = node
                   answer = rv.relative(node)
                   isPronoun = True
                if (node.lex in locativePronouns) and (node.morphPOS == 'pn'):
                    mention = node
                    answer = lt.locative(node, linearChunkList, nerDict)
                    isPronoun = True
                if isPronoun:
                    if (not relfile):
                        print(rfp)
                    if (not relsent):
                        print("\tSentence : ", sentence.name)
                    relfile = True
                    relsent = True
                    if (answer is None):
                        print('\t\t', mention.name, "-->", "NO OUTPUT")
                        print("\t\tIncorrect - Out of sentence, Using Classifier ....")
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

                            x = [num, parsedNodes[0], j - parsedNodes[1],
                                int(chunk.upper.name) - parsedNodes[2], parsedNodes[3], parsedNodes[4], anim]
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
                            testingIO.append(
                                [x, clf.predict_proba([x])[0], goldOutput])
                            # print('tesIO after:', len(testingIO))

                        # print('tesIO:', len(testingIO))
                        testingIO = sorted(
                            testingIO, key=lambda y: y[1][1], reverse=True)
                        if testingIO[0][2] == 1:
                            correct += 1
                            print ("Classifier : Correct")
                        else:
                            incorrectClassifier += 1
                            print ("Classifier : Incorrect")

                        OOS += 1
                    else:
                        print('\t\t', mention.name, "-->", answer.name)
                #   ------------- NEW CHECKING METHOD -------------            
                        mentionLinksTo = 0 if mention.getAttribute('crefType') is None else mention.getAttribute('crefType').split(':')[1]
                        chainsWithReferent = set()
                        chainsWithMention = set()
                        chainsWithPrediction = set()

                        if (mention.getAttribute('cref') is not None):
                            for c in mention.getAttribute('cref').split(','):
                                chainsWithMention.add(c.split(':')[1])
                        if (answer.getAttribute('cref') is not None):
                            for c in answer.getAttribute('cref').split(','):
                                chainsWithPrediction.add(c.split(':')[1])
                        for corefChain in doc.coreferenceChainNodeList:
                            for corefEntity in corefChain.nodeList:
                                if corefEntity.uniqueid == mentionLinksTo:
                                    chainsWithReferent.add(corefChain.chainid)
                        
                        # print("\nThe prediction was in : ",end='')
                        # for x in chainsWithPrediction:
                        #     print(x, end=', ')
                        # print("\nThe referent was in : ", end='')
                        # for x in chainsWithReferent:
                        #     print(x, end=', ')
                        # print("\nThe mention was in : ",end='')
                        # for x in chainsWithMention:
                        #     print(x, end=', ')
                        if len(set.intersection(chainsWithPrediction, chainsWithReferent, chainsWithMention)) > 0:
                #   ------------- NEW CHECKING METHOD -------------        
                #   xxxxxxxxxxxxx OLD CHECKING METHOD xxxxxxxxxxxxx
                        # mChains = []
                        # aChains = []
                        # for corefChain in doc.coreferenceChainNodeList:
                        #     for corefEntity in corefChain.nodeList:
                        #         if mention in corefEntity.nodes:
                        #             mChains.append(corefChain)
                        #         if answer in corefEntity.nodes:
                        #             aChains.append(corefChain)
                        # flag = 0
                        # for a in aChains:
                        #     if a in mChains:
                        #         flag = 1
                        # if flag == 1:
                #   xxxxxxxxxxxxx OLD CHECKING METHOD xxxxxxxxxxxxx
                            print("\t\tCorrect")
                            correct += 1
                        else:
                            print("\t\tIncorrect - Wrong Resolution")
                            incorrectWR += 1

print("Correct Total: ", correct)
print("Incorrect via Rules: ", incorrectWR)
print("Out of Scope, given to classifier: ", OOS)
print("Out of Scope, incorrect by classifier: ", incorrectClassifier)

