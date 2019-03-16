from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from os import listdir
import math
import string, time
import sys
from indexingModules_LL import preprocess, createDetailDocsList, createTermList, ceatePostingList, findDocsByQuery, findDocsByQueries, findDocByPhrase
from threading import Thread
from kivy.uix.popup import Popup

exitFlag = 0

class IRsystemListButton(ListItemButton):
    pass
class IRsystemPanel(ListItemButton):
    def __init__(self, **kwargs):
        super(IRsystemPanel, self).__init__(**kwargs)
        self.height = "150dp"
        

class IRsystem(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    directory = ObjectProperty()
    query = ObjectProperty()
    result_list = ObjectProperty()
    message = ObjectProperty()
    limit = ObjectProperty()
    content = ObjectProperty()

    SWFile = 'english-stop.txt'     # get name of stopword file
    DNames = []
    DetailDocList = []
    TermList = []
    PositingList = []

    
    def full_text_IRsystem(self):
        # If a list item is selected
        if self.result_list.adapter.selection:

            # Get the text from the item selected
            selection = self.result_list.adapter.selection[0].text

            with open(self.directory.text + selection[6:21]) as f:
                p = f.read()
            f.close()

            self.content.adapter.data = [p]


    def gen_message(self, m):

        self.message.adapter.data = [m]

        # Reset the ListView
        self.message._trigger_reset_populate()

    def index_IRsystem(self):

        self.content.adapter.data = ['']
        
        dirc = self.directory.text

        self.DNames = listdir(dirc)      # get list of document names in the folder

        with open(self.SWFile) as f1:    # read stop word file
            SW = f1.read()
        f1.close()
        SW = SW.split()

        self.DetailDocList = createDetailDocsList(dirc, SW)    # create [list of term] for each doc in the directory

        self.TermList = createTermList(self.DetailDocList)    # create a list to store all the terms
        
        start = time.time()
        self.PositingList = ceatePostingList(self.TermList, self.DetailDocList)    # create a posting list for storing document id
        end = time.time()
        
        self.gen_message('[Done] Posting list is created in ' + str(round((end - start), 2)) + 's')

          # Opens Popup when called

        
    def search_IRsystem(self):

        self.content.adapter.data = ['']

        self.delete_results()
        
        query = self.query.text.lower()

        phraseBool = 0

        if not query:
            self.gen_message('Please input query')

        else:

            '''    advanced requirement :  phrase query       '''

            if len(query.split()) == 2:
                phrase = query.split()
                results = findDocByPhrase(phrase, self.TermList, self.DetailDocList, self.PositingList)
                phraseBool = 1

                '''    advanced requirement :  composite query - AND       '''

            elif 'and' in query.split():
                queries = query.split(' and ')

                # Document-at-a-time Query processing
                # Ranked by cosine similarity 
                results = findDocsByQueries(queries, self.TermList, self.DetailDocList, self.PositingList)


                '''    advanced requirement :  composite query - OR       '''

            elif 'or' in query.split():
                queries = query.split(' or ')

                results0 = findDocsByQuery(queries[0], self.TermList, self.DetailDocList, self.PositingList)
                results1 = findDocsByQuery(queries[1], self.TermList, self.DetailDocList, self.PositingList)

                if results0 and results1:
                    results = sorted(results0 + results1, key=lambda l:l[1], reverse=True)


                '''    Basic requirement :  single term query       '''

            else:
                # search docs by query, return a list of docs sorted by term frequency.
                results = findDocsByQuery(query, self.TermList, self.DetailDocList, self.PositingList)


            '''         Check the validation of result list         '''

            if results == [] or results == 0:
                self.gen_message('Cannot find any relevant document.')
            else:
                
                self.gen_message('[Done] We found '+str(len(results))+ ' result' + 's'*(len(results)>1) + ' in the collection.')


                '''          If valid, show the result           '''

                resultItem = []
                if phraseBool == 0:
                    for result in results:
                        resultItem.append('Doc : '+self.DNames[result[0]]+'  -  Score : '+str(result[1]))
                else: #phraseBool==1
                    for result in results:
                            resultItem.append('Doc : '+self.DNames[result[0]]+'  -  Position : '+str(result[1]))
                
                # Add the IRsystem to the ListView
                self.result_list.adapter.data.extend(resultItem)
        
                # Reset the ListView
                self.result_list._trigger_reset_populate()

    def delete_results(self, *args):

            # Remove all the item
            self.result_list.adapter.data = []
 
            # Reset the ListView
            self.result_list._trigger_reset_populate()

class IRsystemApp(App):
    def build(self):
        return IRsystem()
 
 
App = IRsystemApp()
 
App.run()