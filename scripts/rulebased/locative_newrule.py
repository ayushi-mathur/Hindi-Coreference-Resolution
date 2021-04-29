import ssfAPI_intra as ssf


def locative(mention, linearChunkList, nothing):  # isnt mention useless then?
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

        iScore = (maxi - i) * (-10)

        if (nChunk.parentRelation in ['k7p', 'k2p']):
            relScore = 200
        else:
            relScore = 0

        animacyScore = 0

        if ('NP' in nChunk.name):
            nScore = 50
            for x in nChunk.nodeList:
                if x.getAttribute('semprop') == 'rest':
                    animacyScore += 1
            animacyScore = animacyScore*200/len(nChunk.nodeList)
        else:
            nScore = -100

        totalScore = iScore + relScore + animacyScore + nScore
        for c in nChunk.nodeList:
            if c.chunkparentRelation == 'head':
                if (totalScore > bestScore):
                    answer = c
                    bestScore = totalScore
        i -= 1
    return answer
