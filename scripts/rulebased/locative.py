import ssfAPI_intra as ssf


def locative(mention, linearChunkList):  # isnt mention useless then?
    nChunk = linearChunkList[-1]  # the last chunk is the one we are on
    answer = None
    sentencesTraversed = 0
    oldSentence = nChunk.upper
    i = len(linearChunkList)-2
    while i >= 0 and sentencesTraversed <= 2:
        nChunk = linearChunkList[i]
        newSentence = nChunk.upper
        if (newSentence is not oldSentence):
            sentencesTraversed += 1
            if (sentencesTraversed > 2):
                return answer
        oldSentence = newSentence
        
        if ('NP' in nChunk.name) and (nChunk.parentRelation in ['k7p', 'k2p']):    
            for c in nChunk.nodeList:
                if c.chunkparentRelation == 'head':
                    answer = c
            return answer
        i -= 1
