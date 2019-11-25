#Import required packages
import json
import pymongo
import requests
#Import secrets
import mongoSecrets
from objdict import ObjDict
from datetime import datetime #this is optional; used to give automatic timing for inserts

class MongoHelper():
    #define a mongo client with the mongoDB uri
    #This code retrieves the URI from "mongoSecrets.py", which is not displayed on the public repo
    mongo_client = pymongo.MongoClient(mongoSecrets.mlab_uri)
    
    #define the default database
    default_database = mongo_client.backendtestinggg

    #define the collection. This is where your information will go
    db_collection = default_database.mongoDemo

    #create methods to insert elements to the collection
    #this method inserts one entry at a time
    def insertOneEntry(self, entry):
        self.db_collection.insert_one(entry)
    
    #this method inserts multiple entries at a time
    def insertManyEntries(self, entryList):
        self.db_collection.insert_many(entryList)


if __name__ == "__main__":
    #Declare a mongo helper
    mongo_helper = MongoHelper()
    
    print("\n--- Record hours ---\n")

    #create a menu to insert entries in the database (or more specifically, the collection)
    choice = ""
    print("Enter one of the options listed below.\n")

    #Have a list to hold json documents
    entries = []

    while choice != 'q':
        #declare a dictionary object to be our Json file
        json_doc = ObjDict()


        print("\n[1]Enter 1 to enter hours")
        print("[q]Enter q finish")
        
        choice = input("What would you like to do? ")

        if choice == '1':
            json_doc['name'] = input("Enter name: ")
            json_doc['hours'] = input("Enter hours: ")
            json_doc['submissionTime'] = datetime.now()
            
            #tester
            print(json_doc)
            #TODO: add json to list
            entries.append(json_doc)

        elif choice == 'q':
            print("Entries are being submitted.")
            #TODO: perform mongo operations
            # if json list is holding one element, use insert one
            # otherwise, insert_many
            '''#tester
            print("Entries length = ", len(entries))'''

            if(len(entries) == 1): #if there is one entry only, use the insert_one method
                mongo_helper.insertOneEntry(entries[0])
            else: #there is more than one entry, use the insert_many method
                mongo_helper.insertManyEntries(entries)

        
        else:
            print("The entered option is not valid")

    
    
    
    '''json_doc = ObjDict()
    
    json_doc['name'] = input("enter name: \n")
    json_doc['hours'] = input("enter hours: \n")
    json_doc['subTime'] = datetime.now()


    print("\n Json file: \n")
    print(json_doc)'''
