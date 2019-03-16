from os import listdir
import math
import string, time
import sys
from indexingModules_LL import preprocess, createDetailDocsList, createTermList, ceatePostingList, findDocsByQuery, findDocsByQueries, findDocByPhrase

SWFile = 'english-stop.txt'

# show the top 5 result
CUT = 5 
results = []
# check command line argument
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print('Usage: main_LL.py <folder of documents> <max number of results>(optional)')
else:
    DIRC = sys.argv[1]
    if len(sys.argv) == 3:
        CUT = int(sys.argv[2])
    # check directory format
    if DIRC[-1] != '/':
        DIRC += '/'

    FNames = listdir(DIRC)

    # read stop word file
    with open(SWFile) as f1:
        SW = f1.read()
    f1.close()
    SW = SW.split()

    # create [list of term] for each doc for a directory
    detailDocList = createDetailDocsList(DIRC, SW)

    # create a list to store all the terms
    termList = createTermList(detailDocList)

    print('\n[processing] Posting list is creating...')

    # create a posting list for storing document id
    start = time.time()
    postingList = ceatePostingList(termList, detailDocList)
    end = time.time()

    print('\n[Done] Posting list is created in %.2f'%(end - start))

    
    # loop for asking query.
    while True:
        query = input('\nInput : ').lower()

        # To quit, input 'q'
        if query == 'q':
            break

        if not query:
            continue 

        start = time.time()

        '''    advanced requirement :  phrase query       '''
        if len(query.split()) == 2:
            phrase = query.split()
            results = findDocByPhrase(phrase, termList, detailDocList, postingList)


            '''    advanced requirement :  composite query - AND       '''
        elif 'and' in query.split():
            queries = query.split(' and ')
            # Document-at-a-time Query processing
            # Ranked by cosine similarity 
            results = findDocsByQueries(queries, termList, detailDocList, postingList)

            '''    advanced requirement :  composite query - OR       '''
        elif 'or' in query.split():
            queries = query.split(' or ')
            results0 = findDocsByQuery(queries[0], termList, detailDocList, postingList)
            results1 = findDocsByQuery(queries[1], termList, detailDocList, postingList)
            if results0 and results1:
                results = sorted(results0 + results1, key=lambda l:l[1], reverse=True)


            '''    Basic requirement :  single term query       '''
        else:
            # search docs by query, return a list of docs sorted by term frequency.
            results = findDocsByQuery(query, termList, detailDocList, postingList)

        end = time.time()

        if results == [] or results == 0:
            print('\nCannot find any relevant document.')
        else:
            print('\nResults are ranked by cosine similarity of tf-idf weight.')

            # print document names that relevant to the query.
            for i, result in enumerate(results):
                if i == CUT:
                    break
                print('Doc : '+FNames[result[0]]+'  -  Score : '+str(result[1]))

            print('\n[Done] We found ', len(results), ' result' + 's'*(len(result)>1) + ' in the collection.')
            if len(results) < CUT:
                CUT0 = len(results)
            else: CUT0 = CUT
            print('[Done] Top ', CUT0, ' result' + 's'*(len(results)>1) + ' are shown.')
            print('[Done] Time used: %.2fs.'%(end-start))