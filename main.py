import string, time
import sys
from os import listdir
from indexingModules import preprocess, createDetailDocsList, createTermList, createTDM, findDocsByQuery, ceatePostingList

SWFile = 'english-stop.txt'
TDM = []
resultList = []

# check command line argument
if len(sys.argv) != 2:
    print('Usage: main.py <directory of documents>')
else:
    DIRC = sys.argv[1]
    # check directory format
    if DIRC[-1] != '/':
        DIRC += '/'

    FNames = listdir(DIRC)

    # open stop word file
    with open(SWFile) as f1:
        SW = f1.read()
    f1.close()
    SW = SW.split()

    # create [list of term] for each doc for a directory
    detailDocList = createDetailDocsList(DIRC, SW)

    # create a list to store all the terms
    termList = createTermList(detailDocList)

    # [Done] exited with code=0 in 0.475 seconds
    # Total 7217 terms
    # Size of TDM  = 200 * 7217 ~= 1,400,000 (one million) 

    s = time.time()
    postingList = ceatePostingList(termList, detailDocList)
    e = time.time()

    '''                 TDM

    # create a 2d list for Term-Document Matrix(TDM)

    start = time.time()
    TDM = createTDM(termList, detailDocList)
    end = time.time()

    print('Time for creating TDM: ', end-start)
    # [Done] exited with code=0 in 4.937 seconds
    # Size of TDM  = 200 * 7217 ~= 1,400,000 (one million) 
    '''

    print('Time for creating postingList: ', e-s)
    # loop for asking query.
    while True:
        query = input('Query : ')

        # search docs by query, return a list of docs sorted by term frequency.
        results = findDocsByQuery(query, termList, detailDocList, postingList)
        if results == [] or results == 0:
            print('Cannot find any relevant document.')
        else:
            print('Results are ranked by term frequency.')
            print(results)

            # print document names that relevant to the query.
            for result in results:
                print('File : '+FNames[result[0]]+', TF : '+str(result[1]))



'''
c=0
postingList = termList
for term in postingList:
    node = term.head.next
    while node :
        print('fname : '+FNames[node.docId]+', Weight: ', node.weight )
        node = node.next
        c+=1
'''
# total 21212 nodes stored in posting list
# each node has docId and weight and address
# 7000 PostingList objects, each of them has term and length and 2 address
# 20000*3+7000*4 = 60000+28000 = 88000