import ssfAPI_intra as ssf
complementizer = 'कि'


def firstperson(mention):
    # mention is a ssf.Node_vandan object
    node = mention  # start at mention node
    while (node.lex != complementizer) and (node.parent != node):
        node = node.parent
    if node.parent == node:
        return None
    while (node.morphPOS != 'v'):
        node = node.parent
    cList = node.childList
    for c in cList:
        if c.parentRelation == 'k1':
            answer = c
            return answer
    return None
