import ssfAPI_intra as ssf

def relative(mention):
    #mention is a ssf.Node_vandan object
    node = mention  #start at mention node
    chunk = node.upper
    flagR = 1
    while(flagR):
        #if node.morphPOS == 'v':
        if ((node.type == 'CC') or (node.type == 'VM')):

            if node.parentRelation == 'nmod__relc':
                flagR = 0
                
                return node.parent

            
        if (node.parent == node):
            for child in node.childList:
                if child.parentRelation == 'k1':
                    return child
                if child.parentRelation == 'r6':
                    return child
                if child.parentRelation == 'k2':
                    return child
                if child.parentRelation == 'k4':
                    return child
            flagR = 0
        else:
            node = node.parent

