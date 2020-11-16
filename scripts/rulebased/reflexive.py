import ssfAPI_intra as ssf
reflexives=['अपनी', 'अपने', 'अपना', 'स्वयं', 'खुद', 'खुद']

def reflexive(mention, prev_sent, prev_prev_sent):
    node=mention
    chunk_mention = node.upper
    sent_mention = chunk_mention.upper
    verb=None
    while(node.type != 'VM'):
        node=node.parent
    for child in node.childList:
        if child.parentRelation == 'k1' and child!=mention:
            return child
    if prev_sent is None:
        return None
    for chunk in prev_sent.nodeList:
        for word in chunk.nodeList:
            if word.type == 'VM':
                verb=word

    for child in verb.childList:
        if child.morphPOS=='n' and child.parentRelation == 'k1':
            return child
    if prev_prev_sent is None:
        return None
    for chunk in prev_prev_sent.nodeList:
        for word in chunk.nodeList:
            if word.type == 'VM':
                verb=word

    for child in verb.childList:
        if child.morphPOS=='n' and child.parentRelation == 'k1':
            return child
    return None