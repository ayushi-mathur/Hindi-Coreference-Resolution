import sys
sys.path
sys.path.append('./scripts/ssfapi/')
import ssfAPI_intra as ssf

fl = ssf.folderWalk('./data')

outFile = open('taggedPronouns.txt', 'w')

reflexivePronouns = ['अपनी', 'अपने', 'अपना', 'स्वयं', 'खुद', 'खुद']
relativePronouns = ['जो', 'जोकि', 'जहाँ', 'जिधर', 'जितना', 'जितने', 'जैसा', 'जैसे', 'जिसको', 'जिसके',
                    'जिस', 'जिसे', 'जिससे', 'जिसकी', 'जिसका', 'जिसने', 'जिन्हें', 'जिन्होंने', 'जिसमें', 'जिनमें', 'जिनकी']
firstPronouns = ['हमसे', 'हमारे', 'मेरा', 'मेरी', 'मेरे', 'हम', 'हमारा',
                 'हमने', 'मुझे', 'मैं', 'मुझ', 'मैने', 'हमें', 'मैंने', 'हमारी']
secondPronouns = ['आप', 'आपस', 'आपकी', 'आपके', 'आपको', 'आपका']
thirdPronouns = ['‌‌वह', 'वे', 'वो', 'उसको', 'उसने', 'उससे', 'उसका',
                 'उसकी', 'उसके', 'उन', 'उनको', 'उन्होंने', 'उनसे', 'उनका', 'उनकी', 'उनके']
locativePronouns = ['वहाँ', 'वहां', 'वहीं', 'यहीं', 'यहाँ',
                    'यहां', 'कहीं', 'इसमें', 'उसमें', 'इनमें']


pronouns = set()
reflexives = set()
relatives = set()
thirdPerson = set()
firstPerson = set()
secondPerson = set()
locatives = set()
for rfp in fl:
    doc = ssf.Document(rfp)
    for s in doc.nodeList:
        for c in s.nodeList:
            for n in c.nodeList:
                if n.type == 'PRP' and n.getAttribute('cref') is not None:
                    pronouns.add(n.lex)

pronouns2 = set.union(set(), pronouns)

for p in pronouns2:
    if p in reflexivePronouns or p in relativePronouns or p in firstPronouns or p in secondPronouns or p in locativePronouns or p in thirdPronouns:
        pronouns.remove(p)
print(pronouns)
for i, p in enumerate(pronouns):
    print(p)
    cat = input(
        "1. fp   2. sp   3. tp   4. reflexive   5. relative   6. locative   None. None:")
    if cat != '':
        cat = int(cat)
    if (cat == 1):
        firstPerson.add(p)
    elif (cat == 2):
        secondPerson.add(p)
    elif (cat == 3):
        thirdPerson.add(p)
    elif (cat == 4):
        reflexives.add(p)
    elif (cat == 5):
        relatives.add(p)
    elif (cat == 6):
        locatives.add(p)
    else:
        pass
