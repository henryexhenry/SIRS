import string
from os import listdir
from indexingModules import preprocess, createDetailDocsList, createTermList

DIRC = 'data/'
DOC = 'data/D0601.M.250.A.A'
SWFile = 'english-stop.txt'
TDM = []

with open(SWFile) as f1:
    SW = f1.read()
f1.close()
SW = SW.split()

detailDocList = createDetailDocsList(DIRC, SW)

termList = createTermList(detailDocList)
print(termList)
# [Done] exited with code=0 in 0.475 seconds
# Total 7217 terms
# Size of TDM  = 200 * 7217 ~= 1,400,000 (one million) 

