# A Simple Index and Query System
## System work flow
### 1. preprocessing docs
- read docs from doc directory
- preprocessing docs
    - Remove punctuations & numbers
    - Convert letters into lowercase

### 2. remove stopwords
- read stopword file
- create term list and remove stopwords and duplicates
    - remove stopword by loop and check
    - remove duplicate by set operation
- sort term list alphabetically

### 3. indexing with term frequency
- create a 2d list as Term-Document Matrix(TDM) to store the term frequency (tf) within each doc
- compare term list with docs, mark the tf into TDM

### 4. Searching
- user gives a query
- start searching the query in TDM
- print out the relevant doc names ranked by tf

## Usage:
### 1. Document directory is needed.
```
> python main.py <doc directory>
```
### 2. Query to search.
You will be continuesly asked for a query.

To exit, press ```ctrl + z``` and ```enter```.

## Modules used
- string
- sys
- os