import ssfAPI_intra as ssf

locativePronouns = ['वहाँ', 'वहां', 'वहीं', 'यहीं', 'यहाँ', 'यहां', 'कहीं', 'इसमें', 'उसमें', 'इनमें']

def locative(mention, linearChunkList, nerDict):  # isnt mention useless then?
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
        
        for c in nChunk.nodeList:
            if c.lex in locativePronouns:
                answer = c
                return c

        for c in nChunk.nodeList:
            ne = nerDict.get(c.lex)
            if ne == 'location':
                answer = c
                return answer
        if (nChunk.parentRelation in ['k7p', 'k2p']):    
            for c in nChunk.nodeList:
                if c.chunkparentRelation == 'head':
                    answer = c
            return answer 
        
        i -= 1
