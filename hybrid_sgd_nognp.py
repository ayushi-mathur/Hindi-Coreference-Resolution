from sklearn.linear_model import SGDClassifier
import sys
sys.path
sys.path.append('./scripts/ssfapi/')
import ssfAPI_intra as ssf

import scripts.rulebased.relative as rv
import scripts.rulebased.reflexive as rx
import scripts.rulebased.locative_newrule as lt
import scripts.rulebased.thirdperson as tp
import scripts.rulebased.secondperson as sp
import scripts.rulebased.firstperson as fp

# ---------- CLASSIFIER TRAINING AREA -------------------

pronounsList = ['NULL', 'मैं', 'दैट', 'उसकी', 'उसके', 'जोकि', 'जहां', 'परस्पर', 'उसी', 'हमें', 'खुद', 'मेरा', 'यह', 'इससे', 'मुझे', 'इसे', 'इनसे', 'मुझ', 'इनको', 'कुछ', 'इस', 'सुपर', 'मेरी', 'उनमें', 'जो', 'जहाँ', 'तभी', 'तहां', 'जैसा', 'यही', 'दूसरे', 'यहीं', 'इसमें', 'ऐसी', 'ऐसा', 'आपकी', 'इसको', 'वहीं', 'इनकी', 'इनका', 'उन्हें', 'जिसमें', 'मैंने', 'आपको', 'इनके', 'जिसके', 'अपनी', 'अपना', 'वही', 'मैने', 'यहां', 'इसके', 'जिन्होंने', 'किसको', 'उनसे', 'जिसका', 'इसी', 'इसलिए', 'वहां', 'सभी', 'उसने', 'किसे', 'जिसने', 'उसे', 'उसका',
                'आपका', 'इसकी', 'अपने', 'जिन्हें', 'यहाँ', 'इतना', 'आपके', 'उनका', 'कोई', 'मेरे', 'इसका', 'वो', 'कहीं', 'ऐसे', 'क्या', 'जिन', 'तब', 'कब', 'एक', 'किस', 'हमारी', 'दिस', 'किसने', 'जब', 'उनको', 'सब', 'इसने', 'जिससे', 'आप', 'आपस', 'हम', 'जिनमें', 'हमारे', 'कभी', 'जिनकी', 'इन', 'किन', 'इनमें', 'किसी', 'वे', 'स्वयं', 'अभी', 'उस', 'हमारा', 'हमने', 'इसीलिए', 'सबको', 'सबके', 'वह', 'वहाँ', 'उनकी', 'जिसको', 'तो', 'जिस', 'ये', 'इन्हीं', 'उन', 'अब', 'जिसकी', 'उन्होंने', 'इन्हें', 'हमसे', 'उनके', 'उससे', 'उसमें', 'जिसे', 'ने']

reflexivePronouns = ['अपनी', 'अपने', 'अपना', 'स्वयं', 'खुद']
relativePronouns = ['जो', 'जोकि', 'जहाँ', 'जिधर', 'जितना', 'जितने', 'जैसा', 'जैसे', 'जिसको', 'जिसके',
                    'जिस', 'जिसे', 'जिससे', 'जिसकी', 'जिसका', 'जिसने', 'जिन्हें', 'जिन्होंने', 'जिसमें', 'जिनमें', 'जिनकी']
firstPronouns = ['हमसे', 'हमारे', 'मेरा', 'मेरी', 'मेरे', 'हम', 'हमारा',
                 'हमने', 'मुझे', 'मैं', 'मुझ', 'मैने', 'हमें', 'मैंने', 'हमारी']
secondPronouns = ['आप', 'आपस', 'आपकी', 'आपके', 'आपको', 'आपका']
thirdPronouns = ['‌‌वह', 'वे', 'वो', 'उसको', 'उसने', 'उससे', 'उसका',
                 'उसकी', 'उसके', 'उन', 'उनको', 'उन्होंने', 'उनसे', 'उनका', 'उनकी', 'उनके']
locativePronouns = ['वहाँ', 'वहां', 'वहीं', 'यहीं', 'यहाँ',
                    'यहां', 'कहीं', 'इसमें', 'उसमें', 'इनमें']

nerDict = {}
nerBag = open('nerBag', 'r')
for line in nerBag.readlines():
    nerDict[line.split(' ')[0]] = line.split(' ')[1].strip()

karaka_list = ['r6-k2', 'k7tu', 'k7', 'k1s', 'k7a', 'k3', 'pk1', 'k1u', 'k3u', 'k5', 'r6v', 'r6',  'k2s',  'k4a',
               'nmod__relc', 'k2p', 'k2u', 'k7pu', 'r6-k1', 'k7p', 'nmod__adj', 'nmod', 'k7t', 'k4',  'k7u', 'k2',   'k2g', 'k1']
karaka_length = len(karaka_list)

correctCount = {"Reflexive":0, "Relative":0,"First":0,"Second":0,"Third":0,"Locative":0,"Unknown":0}
incorrectCount = {"Reflexive":0, "Relative":0,"First":0,"Second":0,"Third":0,"Locative":0, "Unknown":0}

nerCategory = {
    'time': -3,
    'measure': -2,
    'number': -1,
    'null': 0,
    'person': 1,
    'location': 2,
    'organization': 3
}


def nerCategoryId(lex):
    named_entity = nerDict.get(lex)
    if named_entity is None:
        named_entity = 0
    else:
        named_entity = nerCategory.get(named_entity)
    return named_entity


fl = ssf.folderWalk('./trainingdata')


trainingInput = []
trainingOutput = []
y = 0
w = 0
totalPronouns = 0
top = [0, 0, 0, 0, 0]

nouns_list = ['NN', 'NNP', 'NNPC', 'PRP']

pronounTypeDict = {1:"reflexive",2:"relative",3:"locative",4:"first",5:"second",6:"third"}

for rfp in fl:

    linearNodeList = []  # Chain ID of every node
    linearChunkList = []
    nodeFeatureList = []

    doc = ssf.Document(rfp)
    for s in doc.nodeList:
        for c in s.nodeList:
            linearChunkList.append(c)

    for i, c in enumerate(linearChunkList):
        for n in c.nodeList:
            if n.type in nouns_list and (n.chunkparentRelation == 'head' or n.type == 'PRP'):
                pass
            else:
                continue
            if n.getAttribute('cref') is not None and (n.getAttribute('cref') != ''):
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


            named_entity = nerCategoryId(n.lex)

            if n.parentRelation in karaka_list:
                pernum = karaka_list.index(n.parentRelation)
            else:
                pernum = 0

            nodeFeatureList.append(
                [num, i, int(c.upper.name), named_entity, nouns_list.index(n.type), pernum])

            if (n.type == 'PRP') and (n.getAttribute('cref') is not None) and (n.getAttribute('cref') != ''):
                totalPronouns += 1
                for k, parsedNodes in enumerate(nodeFeatureList):
                    if (i - parsedNodes[1] < 1):
                        continue

                    prn_lex = n.lex
                    if prn_lex in reflexivePronouns:
                        pType = 1
                    elif prn_lex in relativePronouns:
                        pType = 2
                    elif prn_lex in locativePronouns:
                        pType = 3
                    elif prn_lex in firstPronouns:
                        pType = 4
                    elif prn_lex in secondPronouns:
                        pType = 5
                    elif prn_lex in thirdPronouns:
                        pType = 6
                    else:
                        pType = 0

                    pType = pType/6

                    trainingInput.append([num, parsedNodes[0], i - parsedNodes[1], int(c.upper.name) - parsedNodes[2],
                                          parsedNodes[3], named_entity, pType, parsedNodes[5], parsedNodes[4], pronounsList.index(prn_lex)])

                    temp = []
                    for cref in n.getAttribute('cref').split(','):
                        temp.append(cref.split(':')[1])
                    if len(set.intersection(set(temp), set(linearNodeList[k]))):
                        trainingOutput.append(1)
                        y += 1
                    else:
                        trainingOutput.append(0)
                        w += 1


clf = SGDClassifier(loss="log",penalty="l2",max_iter=1000)
clf = clf.fit(trainingInput, trainingOutput)

# ---------- END OF CLASSIFIER TRAINING AREA -------------------

fileList = ssf.folderWalk('./testingdata/')

correct = 0
OOS = 0
incorrectWR = 0
incorrectClassifier = 0


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
                use_classifier_flag = False
                isPronoun = False

                if node.type in nouns_list and node.chunkparentRelation == 'head':
                    pass
                else:
                    continue
                if node.getAttribute('cref') is not None and (node.getAttribute('cref') != ''):
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

                named_entity = nerCategoryId(node.lex)

                if node.parentRelation in karaka_list:
                    pernum = karaka_list.index(node.parentRelation)
                else:
                    pernum = 0
                    
                nodeFeatureList.append([num, j, int(
                    chunk.upper.name), named_entity, nouns_list.index(node.type), pernum, node])
                    
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
                    answer = tp.thirdperson(
                        node, doc.nodeList[i-1] if i > 0 else None, doc.nodeList[i-2] if i > 1 else None, doc.nodeList[i-3] if i > 2 else None)
                    isPronoun = True
                if node.lex in reflexivePronouns:
                    mention = node
                    answer = rx.reflexive(
                        node, doc.nodeList[i-1] if i > 0 else None, doc.nodeList[i-2] if i > 1 else None)
                    isPronoun = True
                if (node.lex in relativePronouns):
                    mention = node
                    answer = rv.relative(node)
                    isPronoun = True
                if (node.lex in locativePronouns):
                    mention = node
                    answer = lt.locative(node, linearChunkList, nerDict)
                    isPronoun = True
                    

                if isPronoun and len(nodeFeatureList) > 0:
                    mentionLex = mention.lex
                    if mentionLex in reflexivePronouns:
                        mentionType = "Reflexive"
                    elif mentionLex in relativePronouns:
                        mentionType = "Relative"
                    elif mentionLex in locativePronouns:
                        mentionType = "Locative"
                    elif mentionLex in firstPronouns:
                        mentionType = "First"
                    elif mentionLex in secondPronouns:
                        mentionType = "Second"
                    elif mentionLex in thirdPronouns:
                        mentionType = "Third"
                    else:
                        mentionType = "Unknown"
                    mentionLinksTo = 0 if mention.getAttribute(
                            'crefType') is None else mention.getAttribute('crefType').split(':')[1]
                    if (not relfile):
                        print(rfp)
                    if (not relsent):
                        print("\tSentence : ", sentence.name)
                    relfile = True
                    relsent = True
                    if (answer is None):
                        print('\t\t', mention.name, "-->", "NO OUTPUT")
                        if (mentionLinksTo == 0):
                            print ("\t\tCorrect - There was no anaphora")
                            correct += 1
                            continue
                        print(
                            "\t\tIncorrect - Out of sentence, Using Classifier ....")
                        testingIO = []
                        goldOutput = []

                        mention = node
                        # ------------------------------------------------
                        for k, parsedNodes in enumerate(nodeFeatureList[:-1]):
                            if (j - parsedNodes[1] < 1) and (j - parsedNodes[1] > 60):
                                continue

                            if node.parentRelation in karaka_list:
                                pernum = karaka_list.index(node.parentRelation)
                            else:
                                pernum = 0

                            prn_lex = node.lex
                            if prn_lex in reflexivePronouns:
                                pType = 1
                            elif prn_lex in relativePronouns:
                                pType = 2
                            elif prn_lex in locativePronouns:
                                pType = 3
                            elif prn_lex in firstPronouns:
                                pType = 4
                            elif prn_lex in secondPronouns:
                                pType = 5
                            elif prn_lex in thirdPronouns:
                                pType = 6
                            else:
                                pType = 0


                            x = [num, parsedNodes[0], (j - parsedNodes[1]), (int(chunk.upper.name) - parsedNodes[2]),
                                parsedNodes[3], named_entity, pType, parsedNodes[5], parsedNodes[4], pronounsList.index(node.lex)]

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
                                [x, clf.predict_proba([x])[0], goldOutput, parsedNodes[6]])
                            # print('tesIO after:', len(testingIO))

                        # print('tesIO:', len(testingIO))
                        testingIO = sorted(
                            testingIO, key=lambda y: y[1][1], reverse=True)

                        if testingIO[0][2] == 1:
                            correctCount[mentionType] +=1
                            print("\t\tCORRECT CLASSED")
                            correct += 1
                        else:
                            incorrectCount[mentionType]+=1
                            print("\t\tINCORRECT CLASSED")
                            incorrectClassifier += 1
                        print(sentence.name,")",sentence.text)
                        print(node.upper.upper.name,':',node.lex,'-->',testingIO[0][3].upper.upper.name,':',testingIO[0][3].lex)

                        OOS += 1
                        use_classifier_flag = True
                    else:
                        print('\t\t', mention.name, "-->", answer.name)
                #   ------------- NEW CHECKING METHOD -------------
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
                            if not use_classifier_flag:
                                print("\t\tCorrect")
                                correct += 1
                                correctCount[mentionType]+=1
                            else:
                                print("\t\tIT WAS CORRECT WITH RULES!")
                        else:
                            if not use_classifier_flag:
                                print("\t\tIncorrect - Wrong Resolution")
                                incorrectWR += 1
                                incorrectCount[mentionType]+=1
                            else:
                                print("\t\tIT WAS INCORRECT WITH RULES!")


print("Correct Total: ", correct)
print("Incorrect via Rules: ", incorrectWR)
print("Out of Scope, given to classifier: ", OOS)
print("Out of Scope, incorrect by classifier: ", incorrectClassifier)
totalCount = {}
print("Right")
for x,y in correctCount.items():
    print('\t',x,":",y)
    totalCount[x] = y
print("Wrong")
for x,y in incorrectCount.items():
    print('\t',x,":",y)
    totalCount[x] += y
print("Total", sum(totalCount.values()))
for x,y in totalCount.items():
    print('\t',x,":",y)
print("Percentage", (sum(correctCount.values())/sum(totalCount.values())) * 100)
for x,y in totalCount.items():
    print('\t',x,':',(correctCount[x]/y)*100)
