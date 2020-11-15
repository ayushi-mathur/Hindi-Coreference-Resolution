complementizer = 'कि'

import ssfAPI_intra as ssf

def secondperson(mention):
    #mention is a ssf.Node_vandan object
    node = mention  #start at mention node
    while (node.name != complementizer) and (node.parent != node):
        node = node.parent
    if node.parent == node:
        return None
    while (node.morphPOS != 'v'):
        node = node.parent
    cList = node.childList
    for c in cList:
        if c.parentRelation == 'k4':
            answer = c
            return answer
    return None
