from os import listdir
import math
import string, time
import sys

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

def findDocsByQuery(query, termList, detailDocList, postingList):
    res = []
    query = query.lower()

    t = termList.index(query)

    # Linked list approach
    node = postingList[t].head.next
    while node:
        res.append([node.docId, node.weight])
        node = node.next

    return sorted(res, key=lambda l:l[1], reverse=True)


STOP = 'english-stop.txt'

# check command line argument
if len(sys.argv) != 2:
    print('Usage: main.py <folder of documents>')
else:
    FOLDER = sys.argv[1]
    # check directory format
    if FOLDER[-1] != '/':
        FOLDER += '/'

    FILEs = listdir(FOLDER)

    # open stop word file
    with open(STOP) as f1:
        SW = f1.read()
    f1.close()
    SW = SW.split()

    # create [list of term] for each doc for a directory
    detailDocList = createDetailDocsList(FOLDER, SW)

    # create a list to store all the terms
    termList = createTermList(detailDocList)
 
    # create a posting list for storing document id
    postingList = ceatePostingList(termList, detailDocList)
    
    
    # loop for asking query.
    while True:
        query = input('Input : ')

        # search docs by query, return a list of docs sorted by term frequency.
        results = findDocsByQuery(query, termList, detailDocList, postingList)
        if results == [] or results == 0:
            print('Cannot find any relevant document.')
        else:
            print('Results are ranked by term frequency.')

            # print document names that relevant to the query.
            for result in results:
                print('Doc : '+FILEs[result[0]]+'\nTF : '+str(result[1]))
