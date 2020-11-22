import sys
sys.path
sys.path.append('./scripts/ssfapi/')
import ssfAPI_intra as ssf

import scripts.rulebased.relative as rv
import scripts.rulebased.reflexive as rx
import scripts.rulebased.locative as lt
import scripts.rulebased.secondperson as sp
import scripts.rulebased.firstperson as fp



reflexivePronouns = ['अपनी', 'अपने', 'अपना', 'स्वयं', 'खुद', 'खुद']
relativePronouns = ['जो', 'जोकि', 'जहाँ', 'जिधर', 'जितना', 'जितने', 'जैसा', 'जैसे', 'जब', 'जिसको', 'जिसके',
                    'जिस', 'जिसे', 'जिससे', 'जिसकी', 'जिसका', 'जिसने', 'जिन्हें', 'जिन्होंने', 'जिसमें', 'जिनमें', 'जिनकी']
firstPronouns = ['हमसे', 'हमारे', 'मेरा', 'मेरी', 'मेरे', 'हम', 'हमारा',
                 'हमने', 'मुझे', 'मैं', 'मुझ', 'मैने', 'हमें', 'मैंने', 'हमारी']
secondPronouns = ['आप', 'आपस', 'आपकी', 'आपके', 'आपको', 'आपका']
locativePronouns = ['वहाँ', 'वहां', 'वहीं', 'यहीं', 'यहाँ',
                    'यहां', 'कहीं', 'इसमें', 'उसमें', 'इनमें']

fileList = ssf.folderWalk('./data/')


mrpair = []

correct = 0
incorrectOOS = 0
incorrectWR = 0


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
                isPronoun = False
                # if node.name in firstPronouns:
                #     mention = node
                #     answer = fp.firstperson(node)
                #     isPronoun = True
                # if node.name in secondPronouns:
                #     mention = node
                #     answer = sp.secondperson(node)
                #     isPronoun = True
                # if node.name in reflexivePronouns:
                #     mention = node
                #     answer = rx.reflexive(
                #         node, doc.nodeList[i-1] if i > 0 else None, doc.nodeList[i-2] if i > 1 else None)
                #     isPronoun = True
                if (node.name in relativePronouns) and (node.morphPOS == 'pn'):
                    mention = node
                    answer = rv.relative(node)
                    isPronoun = True
                # if (node.lex in locativePronouns) and (node.morphPOS == 'pn'):
                #     mention = node
                #     answer = lt.locative(node, linearChunkList)
                #     isPronoun = True
                if isPronoun:
                    if (not relfile):
                        print(rfp)
                    if (not relsent):
                        print("\tSentence : ", sentence.name)
                    relfile = True
                    relsent = True
                    if (answer is None):
                        print('\t\t', mention.name, "-->", "NO OUTPUT")
                        print("\t\tIncorrect - Out of sentence")
                        incorrectOOS += 1
                    else:
                        print('\t\t', mention.name, "-->", answer.name)
                #   ------------- NEW CHECKING METHOD -------------            
                        # mentionLinksTo = 0 if mention.getAttribute('crefType') is None else mention.getAttribute('crefType').split(':')[1]
                        # chainsWithReferent = set()
                        # chainsWithMention = set()
                        # chainsWithPrediction = set()

                        # if (mention.getAttribute('cref') is not None):
                        #     for c in mention.getAttribute('cref').split(','):
                        #         chainsWithMention.add(c.split(':')[1])
                        # if (answer.getAttribute('cref') is not None):
                        #     for c in answer.getAttribute('cref').split(','):
                        #         chainsWithPrediction.add(c.split(':')[1])
                        # for corefChain in doc.coreferenceChainNodeList:
                        #     for corefEntity in corefChain.nodeList:
                        #         if corefEntity.uniqueid == mentionLinksTo:
                        #             chainsWithReferent.add(corefChain.chainid)
                        
                        # print("\nThe prediction was in : ",end='')
                        # for x in chainsWithPrediction:
                        #     print(x, end=', ')
                        # print("\nThe referent was in : ", end='')
                        # for x in chainsWithReferent:
                        #     print(x, end=', ')
                        # print("\nThe mention was in : ",end='')
                        # for x in chainsWithMention:
                        #     print(x, end=', ')
                        # if len(set.intersection(chainsWithPrediction, chainsWithReferent, chainsWithMention)) > 0:
                #   ------------- NEW CHECKING METHOD -------------        
                #   xxxxxxxxxxxxx OLD CHECKING METHOD xxxxxxxxxxxxx
                        mChains = []
                        aChains = []
                        for corefChain in doc.coreferenceChainNodeList:
                            for corefEntity in corefChain.nodeList:
                                if mention in corefEntity.nodes:
                                    mChains.append(corefChain)
                                if answer in corefEntity.nodes:
                                    aChains.append(corefChain)
                        flag = 0
                        for a in aChains:
                            if a in mChains:
                                flag = 1
                        if flag == 1:
                #   xxxxxxxxxxxxx OLD CHECKING METHOD xxxxxxxxxxxxx
                            print("\t\tCorrect")
                            correct += 1
                        else:
                            print("\t\tIncorrect - Wrong Resolution")
                            incorrectWR += 1
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
