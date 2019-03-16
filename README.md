# A Simple Information Retrieval System
## Indexing
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

## Searching
- **single query**
    - findDocsByQuery() function in indexingModules_LL.py file.
    - start searching the doc which has non-zero weight for the query
    - print out the relevant doc names ranked by weights
- **composite query**
    - findDocsByQueries() function in indexingModules_LL.py file.
    - search the docs which has non-zero weight for each query
    - compute weight of all queries for each doc
        - 'AND' operation
            - apply intersect operation to the set of doc weight for each query for finding common docs
            - add up all query weights for each doc
        - 'OR' operation
            - perform single query search for each query
    - print out the relevant doc names ranked by weights
- **phrase query**
    - findDocByPhrase() function in indexingModules_LL.py file.
    - Compare the linked list of each word.
    - Find common documents.
    - Compare two position lists in two linked list from the doc.
    - Find doc with position difference in 1.  


## Usages (Two choises of interface):
### - **Dos interface:**
### 1. Document directory is needed.
Document directory is the folder which you store the documents you are going to index.
- For the Linked list approach:
    ```
    > python main_LL.py <doc directory>
    ```
- Or for the 2-d list approach:
    ```
    > python main_2dL.py <doc directory>
    ```

### 2. Query to search.
You can now search documents by your queries iteratively.

To exit, press ```q``` and hit ```enter```.

## Modules used
- string
- math
- time
- sys
- os

### - **Kivy interface:**
### 1. Install Kivy
- 1. Ensure you have the latest pip and wheel:
    ```
    python -m pip install --upgrade pip wheel setuptools
    ```
- 2. Install the dependencie
    ```
    python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
    ```
- 3. Install kivy:
    ```
    python -m pip install kivy
    ```
### 2. Run the program
- start running the script
    ```
    python IRsystem.py
    ```
- Click the ```Index``` button for indexing the document in the directory.

- Input query in the ```query``` text space and click ```Search```.

- Select result and hit ```Full text``` for full text of the selected document.