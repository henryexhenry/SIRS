import string
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

    # create a 2d list for Term-Document Matrix(TDM)
    TDM = createTDM(termList, detailDocList)
    # [Done] exited with code=0 in 4.937 seconds
    # Size of TDM  = 200 * 7217 ~= 1,400,000 (one million) 

    # loop for asking query.
    while True:
        query = input('Query : ')

        # search docs by query, return a list of docs sorted by term frequency.
        results = findDocsByQuery(query, TDM, termList, detailDocList)
        if results == []:
            print('The query is not relevant to any document.')
        else:
            print('Results are ranked by term frequency.')
            print(results)

            # print document names that relevant to the query.
            for result in results:
                print('File : '+FNames[result[0]]+', TF : '+str(result[1]))

