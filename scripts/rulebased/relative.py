import ssfAPI_intra as ssf

def relative(mention):
    #mention is a ssf.Node_vandan object
    node = mention  #start at mention node
    chunk = node.upper
    flagR = 1
    #haha = 0
    while(flagR):
        #print(haha)
        #haha += 1
        #if node.morphPOS == 'v':
        if ((node.type == 'CC') or (node.type == 'VM')):
            #print("hi")

            if node.parentRelation == 'nmod__relc':
                flagR = 0
                '''
                if node.parent.parentRelation == 'rh':
                    for child in node.parent.parent.childList:
                        if child.parentRelation == 'k1' or child.parentRelation == 'pof':
                            return child
                    #return node.parent.parent
                    '''
                
                return node.parent
                '''
            else:
                if node.parent.type == 'VM':
                    for child in node.parent.childList:
                        if child.parentRelation == 'k1':
                            if mention.name != child.name:
                                return child
                                '''

            
        if (node.parent == node):
            flagR = 0
        else:
            node = node.parent

