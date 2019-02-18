import string
from os import listdir

# preprocess doc: 
# 1. remove special characters(,.") 
# 2. convert into lowercase
# (str, []) -> []
def preprocess(p, sw): 
    
    # remove punctuations and numbers
    # convert all words into lowercase
    pp = p.translate(str.maketrans('','',string.punctuation)).lower()
    pp = pp.translate(str.maketrans('','','1234567890'))

    # split p into a list of word
    tl = pp.split() # term list

    # remove stopword
    i = 0
    while i<len(tl):
        if tl[i] in sw:
            tl.pop(tl.index(tl[i]))
        else:
            i+=1

    return tl


# create list of terms for each doc for the directory
# (str, []) -> [][]
def createDetailDocsList(dirc, sw):

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
# ([][]) -> []
def createTermList(docList): 

    termBag = set()

    # merge all terms into a bag
    for doc in docList:
        termBag |= set(doc)

    # convert bag into list and sort it
    termList = list(termBag)
    termList.sort()

    return termList

# create a 2d list for Term-Document Matrix(TDM)
# ([7000], [200][*]) -> [7000][200]
def createTDM(termList, detailDocList): 
    ltl = len(termList)
    lddl = len(detailDocList)
    TDM = [[0 for _ in range(lddl)] for _ in range(ltl)]

    for d, doc in enumerate(detailDocList):
        for term in doc:
            if term in termList:
                t = termList.index(term)
                TDM[t][d] += 1

    return TDM

# search docs by query, return a list of docs sorted by term frequency.
# (str, [][], [], [][]) -> [][]
def findDocsByQuery(query, TDM, termList, detailDocList):

    resultList = []

    if query in termList:
        t = termList.index(query)

        for d, f in enumerate(TDM[t]):
            if f > 0:
                resultList.append([d, f])

    return sorted(resultList, key=lambda l:l[1], reverse=True)