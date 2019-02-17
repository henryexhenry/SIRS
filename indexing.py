import string

with open('data/D0601.M.250.A.A') as f:
    p = f.read()
f.close()

with open('english-stop.txt') as f1:
    sw = f1.read()
f1.close()
sw = sw.split()

# preprocess words in doc: 1. remove special characters(,.") 2. convert into lowercase
p = p.translate(str.maketrans('','',string.punctuation)).lower()
p = p.translate(str.maketrans('','','1234567890'))

# split p into a list of word
p = p.split() 

# if the word is in stopword list, remove it.
i = 0
while i<len(p):
    if p[i] in sw:
        p.pop(p.index(p[i]))
    else:
        i+=1
print(p)

