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
# (str, [][], [], [][]) -> [][]
def findDocsByQuery(query, termList, detailDocList, VSM):
    resultList = []
    if query in termList:
        t = termList.index(query)
    
        if type(VSM[0]) == list:
            # TDM approach
            for d, f in enumerate(VSM[t]):
                if f > 0:
                    resultList.append([d, f])

        else:
            # Linked list approach
            node = VSM[t].head.next
            print(node)
            while node:
                resultList.append([node.docId, node.weight])
                print([node.docId, node.weight])
                node = node.next

        return sorted(resultList, key=lambda l:l[1], reverse=True)
    return 0

class Node:
    def __init__(self, docId, weight=None):
        self.docId = docId
        self.weight = weight
        self.next = None # the pointer initially points to nothing

class PostingList:
    def __init__(self, head):
        self.term = head
        self.length = 0
        self.head = Node(head)
        self.end = self.head
    
    def addNode(self, docId, weight):
        self.end.next = Node(docId, weight)
        self.end = self.end.next
        self.length += 1
    
    def search(self):
        result = []
        curr = self.head.next
        if curr.weight > 0:
            result.append((curr.docId, curr.weight))
        return result
        '''
termList = ['aba', 'abandon', 'abc']
j=0
k=13
for i in range(len(termList)):
    j+=1
    k+=1
    termList[i] = PostingList(i)
    termList[i].addNode(j, k)
    print(termList[i].search())'''

def ceatePostingList(termList, detailDocList):
    N = len(termList)
    postingList = [0 for _ in range(N)]

    for i in range(len(termList)):
        postingList[i] = PostingList(termList[i])
        df=0

        for doc in detailDocList:
            if termList[i] in doc:
                df+=1

        for j, doc in enumerate(detailDocList):
            if termList[i] in doc:

                tf = doc.count(termList[i])
                ifd = math.log(N/df, 10)
                w = tf*ifd
                if w > 0:
                    postingList[i].addNode(j, w)
    return postingList