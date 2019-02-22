import string
from os import listdir
import math

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
    N = len(detailDocList)
    TDM = [[0 for _ in range(N)] for _ in range(ltl)]
    '''
    for d, doc in enumerate(detailDocList):
        for term in doc:
            if term in termList:
                t = termList.index(term)
                TDM[t][d] += 1
    '''
    for t, term in enumerate(termList):
        df = 0
        for doc in detailDocList:
            if term in doc:
                df += 1
        for d, doc in enumerate(detailDocList):
            if term in doc:
                tf = doc.count(term)
                ifd = math.log(N/df, 10)
                w = tf*ifd
                TDM[t][d] = w

    return TDM

# search docs by query, return a list of docs sorted by term frequency.
# VSM for vector space model
# (str, [], [][], [][]/[]) -> []
def findDocsByQuery(query, termList, detailDocList, VSM):
    resultList = []
    query = query.lower()
    queries = [query]

    # composit query with AND operation
    if ' and ' in query.lower():

        queries = query.split(' and ')
        t_idxs = []

        # find document ids which include query terms
        # store document ids into set()
        for q, query_ in enumerate(queries):
            if query_ in termList:
                t_idx = termList.index(query_)
                t_idxs.append(t_idx)
                resultList.append(set())
                for d, w in enumerate(VSM[t_idx]):
                    if w > 0:
                        resultList[q].add(d)
        temp = resultList[0]

        # find common document ids by intersect operation
        for d in range(len(resultList)):
            temp &= resultList[d]

        temp = list(temp)

        # find weights accroding to doc ids.
        resultList = []

        for d in temp:
            sum_w = 0
            for q in t_idxs:
                sum_w += VSM[q][d]
            resultList.append([d, sum_w])

        # return [docid, weight] list sorted by weight
        return sorted(resultList, key=lambda l:l[1], reverse=True)


    elif ' or ' in query.lower():
        queries = query.split(' or ')

    # OR operation : search each query term one-by-one and append them into result list
    for query in queries:
        if query in termList:
            t = termList.index(query)
            for d, w in enumerate(VSM[t]):
                if w > 0:
                    resultList.append([d, w])
        else:
            return 0
    return sorted(resultList, key=lambda l:l[1], reverse=True)



