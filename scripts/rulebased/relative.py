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
        if ((node.type == 'VGF') or (node.type == 'VGNF') or (node.type == 'VM')):
            #print("hi")
            if node.parentRelation == 'nmod__relc':
                flagR = 0
                return node.parent
                
            
        if (node.parent == node):
            flagR = 0
        else:
            node = node.parent

