from os import listdir
import math
import string, time
import sys

class Node:
    def __init__(self, docId, weight=None, listOfPos=[]):
        self.docId = docId
        self.listOfPos = listOfPos
        self.weight = weight
        self.next = None # the pointer initially points to nothing

class PostingList:
    def __init__(self, head):
        self.term = head
        self.df = 0
        self.head = Node(head)
        self.end = self.head
    
    def addNode(self, docId, weight, listOfPos):
        self.end.next = Node(docId, weight, listOfPos)
        self.end = self.end.next
        self.df += 1
    
    def search(self):
        result = []
        curr = self.head.next
        if curr.weight > 0:
            result.append((curr.docId, curr.weight))
        return result

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
                indices = [k for k, x in enumerate(doc) if x == termList[i]]
                tf = doc.count(termList[i])
                idf = math.log(N/df, 10)
                w = tf*idf
                if w > 0:
                    postingList[i].addNode(j, w, indices)

    return postingList

def findDocsByQuery(query, termList, detailDocList, postingList):
    res = []
    query = query.lower()

    try:
        t = termList.index(query)
    except(ValueError):
        return 0

    # Linked list approach
    node = postingList[t].head.next
    while node:
        res.append([node.docId, node.weight])
        node = node.next

    return sorted(res, key=lambda l:l[1], reverse=True)

def findDocsByQueries(queries, termList, detailDocList, postingList):
    queries = [query.lower() for query in queries]

    try:
        t0 = termList.index(queries[0])
        t1 = termList.index(queries[1])
    except(ValueError):
        return 0

    resList = []

    # Linked list approach
    node0 = postingList[t0].head.next
    node1 = postingList[t1].head.next

    while node0 and node1:
        if node0.docId == node1.docId:
            resList.append([node0.docId, node0.weight*math.log(len(detailDocList)/postingList[t0].df, 10) + node1.weight*math.log(len(detailDocList)/postingList[t1].df, 10)])
            node0 = node0.next
            node1 = node1.next
        elif node0.docId < node1.docId:
            node0 = node0.next
        elif node0.docId > node1.docId:
                node1 = node1.next

    return sorted(resList, key=lambda l:l[1], reverse=True)


def findDocByPhrase(phrase, termList, detailDocList, postingList):
    result = []
    res0 = []
    res1 = []
    phrase = [ph.lower() for ph in phrase]

    try:
        t_list = [termList.index(w) for w in phrase]
    except(ValueError):
        return 0

    # Linked list approach
    # find the posting lists of 2 terms
    node0 = postingList[t_list[0]].head.next
    while node0:
        res0.append([node0.docId, node0.weight, node0.listOfPos])
        node0 = node0.next

    node1 = postingList[t_list[1]].head.next
    while node1:
        res1.append([node1.docId, node1.weight, node1.listOfPos])
        node1 = node1.next
    
    # find common docs where both terms appear.
    # first check the shorter posting list
    if len(res0) > len(res1):
        res0_docid = [doc[0] for doc in res0]
        for i, doc in enumerate(res1):
            if res1[i][0] in res0_docid:
                for j in res1[i][2]:
                    if j-1 in res0[res0_docid.index(res1[i][0])][2]: # compare res0 and res1
                        result.append([doc[0],j]) # [docID, position]
    else:   # len(res0) < len(res1)
        res1_docid = [doc[0] for doc in res1]
        for i, doc in enumerate(res0):
            if res0[i][0] in res1_docid:
                for j in res0[i][2]:
                    if j+1 in res1[res1_docid.index(res0[i][0])][2]: # compare res0 and res1
                        result.append([doc[0], j]) # [docID, position]

    return result