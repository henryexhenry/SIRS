# A Simple Index and Query System
### 1. preprocessing docs
- read docs from doc directory
- preprocessing docs
    - Remove punctuations & numbers
    - Convert letters into lowercase

### 2. remove stopwords
- read stopword file
- create term list without stopwords and duplicates
- sort term list alphabetically

### 3. indexing with term frequency
- create a 2d list as Term-Document Matrix(TDM) to store the term frequency (tf) within each doc. 
- compare term list with docs, mark the tf into TDM.

### 4. Searching
- user gives a query
- start searching the query in TDM
- print out the relevant doc name 