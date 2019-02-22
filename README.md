# A Simple Index and Query System
## System workflow
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
- find tf-idf weight (tf for term frequency; idf for inverted document frequency)
- create a 2d list as Term-Document Matrix(TDM) to store the term tf-idf weight within each doc
- compare term list with docs, mark the weight into TDM

### 4. Searching
- single query
    - user gives a query
    - start searching the doc which has non-zero weight for the query
    - print out the relevant doc names ranked by weights
- multiple query 
    - user gives queries
    - search the doc which has non-zero weight for each query
    - compute weight of all queries for each doc
        - 'AND' operation
            - apply intersect operation to the set of doc weight for each query for finding common docs
            - add up all query weights for each doc
        - 'OR' operation
            - perform single query search for each query
    - print out the relevant doc names ranked by weights

## Usage:
### 1. Document directory is needed.
Document directory is the folder which you store the documents you are going to index.
```
> python main.py <doc directory>
```
### 2. Query to search.
You will be continuously asked for a query.

To exit, press ```ctrl + c``` and ```enter```.

## Modules used
- string
- math
- time
- sys
- os