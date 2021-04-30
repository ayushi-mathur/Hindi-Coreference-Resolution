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

nerDict = {}
nerBag = open('nerBag', 'r')
for line in nerBag.readlines():
    nerDict[line.split(' ')[0]] = line.split(' ')[1].strip()


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

fileList = ssf.folderWalk('./testingdata/')


mrpair = []

correct = 0
incorrectOOS = 0
incorrectWR = 0
totalPronouns = 0

correctCount = {"Reflexive":0, "Relative":0,"First":0,"Second":0,"Third":0,"Locative":0,"Unknown":0}
incorrectCount = {"Reflexive":0, "Relative":0,"First":0,"Second":0,"Third":0,"Locative":0, "Unknown":0}

for rfp in fileList:
    relfile = False
    doc = ssf.Document(rfp)
    linearChunkList = []
    linearNodeList = []
    for i, sentence in enumerate(doc.nodeList):
        relsent = False
        for chunk in sentence.nodeList:
            linearChunkList.append(chunk)
            for node in chunk.nodeList:
                if node.type == 'PRP':
                    pass
                else:
                    continue
                isPronoun = False
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
                if (node.lex in relativePronouns):
                    mention = node
                    answer = rv.relative(node)
                    isPronoun = True
                if (node.lex in locativePronouns):
                    mention = node
                    answer = lt.locative(node, linearChunkList, nerDict)
                    isPronoun = True
                if isPronoun:
                    mentionLex = node.lex

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

                    mentionLinksTo = 0 if mention.getAttribute('crefType') is None else mention.getAttribute('crefType').split(':')[1]
                    totalPronouns += 1
                    if (not relfile):
                        print(rfp)
                    if (not relsent):
                        print("\tSentence : ", sentence.name)
                        print(sentence.text)
                    relfile = True
                    relsent = True
                    if (answer is None):
                        print('\t\t', mention.upper.upper.name,':' ,mention.name, "-->", "NO OUTPUT", " pType:",mentionType)
                        if (mentionLinksTo == 0):
                            print ("\t\tCorrect - There was no anaphora")
                            correct += 1
                            correctCount[mentionType] += 1
                            continue
                        print("\t\tIncorrect - Out of sentence")
                        incorrectCount[mentionType] +=1
                        incorrectOOS += 1
                    else:
                        print('\t\t', mention.upper.upper.name,':' ,mention.name, "-->", answer.upper.upper.name,':' ,answer.name, " pType:",mentionType)
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
                            print("\t\tCorrect")
                            correct += 1
                            correctCount[mentionType] += 1
                        else:
                            print("\t\tIncorrect - Wrong Resolution")
                            incorrectWR += 1
                            incorrectCount[mentionType] += 1
                        # print("\t\tThe correct are: ")
                        # for b in mChains:
                        #     for c in b.nodeList:
                        #         for d in c.nodes:
                        #             print(d.name)
    # for m,r in mrpair:
    #     print (m, "-->", r)
print("Correct: ", correct)
print("Incorrect: ", incorrectWR)
print("Out of Scope: ", incorrectOOS)
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