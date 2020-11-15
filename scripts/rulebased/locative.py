import ssfAPI_intra as ssf


def locative(mention, linearChunkList):  # isnt mention useless then?
    nChunk = linearChunkList[-1]  # the last chunk is the one we are on
    answer = None
    sentencesTraversed = 0
    i = len(linearChunkList)-2
    while i >= 0 and sentencesTraversed <= 3:
        if (linearChunkList[i].upper != nChunk.upper):
            sentencesTraversed += 1
        nChunk = linearChunkList[i]
        
        if ('NP' in nChunk.name) and (nChunk.parentRelation in ['k7p', 'k2p']):    
            for c in nChunk.nodeList:
                if c.chunkparentRelation == 'head':
                    answer = c
            return answer
        i -= 1
