import string
from os import listdir

# preprocess doc: 
# 1. remove special characters(,.") 
# 2. convert into lowercase
def preprocess(p, sw): # (str, []) -> []
    
    pp = p.translate(str.maketrans('','',string.punctuation)).lower()
    pp = pp.translate(str.maketrans('','','1234567890'))

    # split p into a list of word
    tl = pp.split() # term list

    # remove stopword from p
    i = 0
    while i<len(tl):
        if tl[i] in sw:
            tl.pop(tl.index(tl[i]))
        else:
            i+=1

    return tl


# create [list of term] for each doc for a directory
def createDetailDocsList(dirc, sw): # (str, []) -> []

    fNames = listdir(dirc)
    detailDocList = []

    for file_ in fNames:
        try:
            with open(dirc + file_) as f:
                p = f.read()
            f.close()
        except:
            print('Invalid document')
            return 0

        tl = preprocess(p, sw)
        detailDocList.append(tl)

    return detailDocList

# create a list to store all the terms
def createTermList(docList): # ([][]) -> []

    termBag = set()

    # merge all terms into a bag
    for doc in docList:
        termBag |= set(doc)

    # convert bag into list and sort it
    termList = list(termBag)
    termList.sort()

    return termList
