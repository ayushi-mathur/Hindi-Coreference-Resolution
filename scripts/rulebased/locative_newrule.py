import ssfAPI_intra as ssf


def locative(mention, linearChunkList, nerDict):  # isnt mention useless then?
    nChunk = linearChunkList[-1]  # the last chunk is the one we are on
    answer = None
    bestScore = -100000
    sentencesTraversed = 0
    oldSentence = nChunk.upper
    maxi = i = len(linearChunkList)-2
    while i >= 0 and sentencesTraversed <= 2:
        nChunk = linearChunkList[i]

        newSentence = nChunk.upper
        if (newSentence is not oldSentence):
            sentencesTraversed += 1
            if (sentencesTraversed > 2):
                return answer
        oldSentence = newSentence

        if (maxi - i) < 3:
            iScore = -50
        else:
            iScore = (maxi - i) * (-10)

        nerScore = 0
        for c in nChunk.nodeList:
            ne = nerDict.get(c.lex)
            if ne == 'location':
                nerScore = 20
                break
            if ne == 'organization':
                nerScore = 10
                break

        if (nChunk.parentRelation in ['k7p', 'k2p']):
            relScore = 220
        else:
            relScore = -400

        animacyScore = 0

        if ('NP' in nChunk.name):
            nScore = 100
            for x in nChunk.nodeList:
                if x.getAttribute('semprop') == 'rest':
                    animacyScore += 1
            animacyScore = animacyScore*100/len(nChunk.nodeList)
        if ('PSP' in nChunk.name):
            nScore = 50
            for x in nChunk.nodeList:
                if x.getAttribute('semprop') == 'rest':
                    animacyScore += 1
            animacyScore = animacyScore*100/len(nChunk.nodeList)
        else:
            nScore = -100

        totalScore = iScore + relScore + animacyScore + nScore + nerScore
        for c in nChunk.nodeList:
            if c.chunkparentRelation == 'head':
                if (totalScore > bestScore):
                    answer = c
                    bestScore = totalScore
        i -= 1
    return answer
