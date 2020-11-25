import ssfAPI_intra as ssf

def gnp_checking(node1,node2):
	if (node2.getAttribute('gender') == 'any'):
		if((node1.getAttribute('number') == node2.getAttribute('number')) and (node1.getAttribute('person') == node2.getAttribute('person'))):
			return True
		else:
			return False
	else:
		if((node1.getAttribute('number') == node2.getAttribute('number')) and (node1.getAttribute('person') == node2.getAttribute('person')) and (node1.getAttribute('gender') == node2.getAttribute('gender'))):
			return True
		else:
			return False

def PrevSentences(mention, sent):
	if sent is None:
		return None
	for chunks in sent.nodeList:
		for word in chunks.nodeList:
			if word.parent == word:
				root = word
	for child in root.childList:
		if child == mention:
			break
		
		if child.parentRelation == 'k1':
			if(gnp_checking(child,mention) == True):
				return child;
		if child.parentRelation == 'k2':
			if(gnp_checking(child,mention) == True):
				return child;
		if child.parentRelation == 'r6':
			if(gnp_checking(child,mention) == True):
				return child;
		if child.parentRelation == 'k4':
			if(gnp_checking(child,mention) == True):
				return child;
		if child.parentRelation == 'k3':
			if(gnp_checking(child,mention) == True):
				return child;
		
	return None

def thirdperson(mention, prev_1_sent, prev_2_sent, prev_3_sent):
	node = mention
	chunk = node.upper
	while (node.parent != node):
		node = node.parent

	answer = PrevSentences(mention,chunk.upper)
	if(answer == None):
		answer = PrevSentences(mention,prev_1_sent)
		if(answer == None):
			answer = PrevSentences(mention,prev_2_sent)
			if(answer == None):
				answer = PrevSentences(mention,prev_3_sent)
	return answer