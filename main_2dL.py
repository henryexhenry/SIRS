import string, time
import sys
from os import listdir
from indexingModules import preprocess, createDetailDocsList, createTermList, createTDM, findDocsByQuery

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

    # get document names in the folder
    FNames = listdir(DIRC)

    # read stop word file
    with open(SWFile) as f1:
        SW = f1.read()
    f1.close()
    SW = SW.split()

    # create [list of term] for each doc in the directory
    detailDocList = createDetailDocsList(DIRC, SW)

    # create a list to store all the terms
    termList = createTermList(detailDocList)
    
    # [Done] exited with code=0 in 0.475 seconds
    # Total 7217 terms
    # Size of TDM  = 200 * 7217 ~= 1,400,000 (one million) 
  
    '''                 TDM                 '''

    # create a 2d list for Term-Document Matrix(TDM)

    start = time.time()
    VSM = createTDM(termList, detailDocList)
    end = time.time()

    print('TDM is successfully created using %.2f s' % (end-start))
    # [Done] exited with code=0 in 4.937 seconds
    # Size of TDM  = 200 * 7217 ~= 1,400,000 
    

    # loop for asking query.
    while True:
        query = input('Query : ')
        
        if query == 'q':
            break
        if not query:
            continue 

        # search docs by query, return a list of docs sorted by term frequency.
        results = findDocsByQuery(query, termList, detailDocList, VSM)
        if results == [] or results == 0:
            print('Cannot find any relevant document.')
        else:
            print('Results are ranked by tf-idf weight.')

            # print document names that relevant to the query.
            for result in results:
                print('File : '+FNames[result[0]]+', Weight : '+str(result[1]))
        print('[Done] We found ', len(results), ' result' + 's'*(len(result)>1) + ' in the collection.\n')