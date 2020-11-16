import sys
sys.path
sys.path.append('./scripts/ssfapi/')

import ssfAPI_intra as ssf
import scripts.rulebased.firstperson as fp
import scripts.rulebased.secondperson as sp
import scripts.rulebased.locative as lt
#import scripts.rulebased.reflexive as rx
import scripts.rulebased.relative as rv


reflexivePronouns = ['अपनी', 'अपने', 'अपना', 'स्वयं', 'खुद', 'खुद']
relativePronouns = ['जो', 'जोकि', 'जहाँ', 'जिधर', 'जितना', 'जितने', 'जैसा', 'जैसे', 'जब', 'जिसको', 'जिसके', 'जिस', 'जिसे', 'जिससे', 'जिसकी', 'जिसका', 'जिसने', 'जिन्हें', 'जिन्होंने', 'जिसमें', 'जिनमें', 'जिनकी']
firstPronouns = ['हमसे', 'हमारे', 'मेरा', 'मेरी', 'मेरे', 'हम', 'हमारा',
                 'हमने', 'मुझे', 'मैं', 'मुझ', 'मैने', 'हमें', 'मैंने', 'हमारी']
secondPronouns = ['आप', 'आपस', 'आपकी', 'आपके', 'आपको', 'आपका']
locativePronouns = ['वहाँ', 'वहां', 'वहीं', 'यहीं', 'यहाँ', 'यहां',
                    'जहां', 'जहाँ', 'कहीं', 'इसमें', 'उसमें', 'इनमें', 'जिसमें']

fileList = ssf.folderWalk('./data/')


mrpair = []

sahi = 0
galatOUT = 0
galatWR = 0


for rfp in fileList:
    relfile = False
    doc = ssf.Document(rfp)
    linearChunkList = []
    linearNodeList = []
    for sentence in doc.nodeList:
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
                #if node.name in reflexivePronouns:
                #    mention = node
                #    answer = rx.reflexive(node)
                #    isPronoun = True
                if ((node.name in relativePronouns) & (node.morphPOS == 'pn')):
                    mention = node
                    answer = rv.relative(mention)
                    isPronoun = True
                # if node.name in locativePronouns:
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
                        galatOUT += 1
                    else:
                        print('\t\t', mention.name, "-->", answer.name)
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
                            print("\t\tCorrect")
                            print("\t\tThe correct are: ")
                            for b in mChains:
                                for c in b.nodeList:
                                    for d in c.nodes:
                                        print(d.name)
                            sahi += 1
                        else:
                            print("\t\tIncorrect - Wrong Resolution")
                            print("\t\tThe correct are: ")
                            for b in mChains:
                                for c in b.nodeList:
                                    for d in c.nodes:
                                        print(d.name)
                            galatWR += 1
    # for m,r in mrpair:
    #     print (m, "-->", r)
print ("Correct: ",sahi)
print ("Incorrect: ",galatWR)
print ("Out: ",galatOUT)
