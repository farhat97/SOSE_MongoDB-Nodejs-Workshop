#Import required packages
import json
import pymongo
import requests
from bson.objectid import ObjectId 
#Import secrets
import mongoSecrets
from objdict import ObjDict
from datetime import datetime #this is optional; used to give automatic timing for inserts

class MongoHelper():
    #define a mongo client with the mongoDB uri
    #this code retrieves the URI from "mongoSecrets.py", which is not displayed on the public repo.
    #therefore, replace "mongoSecrets.mlab_uri" with your mongo uri
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

    #create methods to retrieve elements from the collection
    #this method retrieves and prints all documents in the collection
    def retrieveAllEntries(self):
        '''Summary
            Pymongo creates a cursor to iterate through the collection.
            Iteration can be performed with the find() method.
            By leaving find's filters empty (hence, collection.find({})), this will iterate through the 
            entire collection
        '''
        cursor = self.db_collection.find({})

        #print the results
        for entries in cursor:
            print(entries, "\n")
    
    #this method retrieves and prints a document with a matching name and hours
    def retrieveEntryWithFilter(self, name, hours):
        cursor = self.db_collection.find({"name" : name, "hours" : hours})

        if cursor is None: #TODO
            print("There are no entries with that name.")

        #print the results
        for entries in cursor:
            print(entries, "\n")
    
    #update an entries hours by passing its ID
    def updateOneEntry(self, id, updatedHours):
        #use ObjectId so mongo knows the "_id" tag is the actual id
        #use the $set keyword to change something in the document
        self.db_collection.update_one(
            {"_id" : ObjectId(id)},
            {"$set" : {"hours" : updatedHours}}
        )
    
    #delete an entry based on its ID
    def deleteOneEntry(self, id):
        #use ObjectId so mongo knows the "_id" tag is the actual id
        self.db_collection.delete_one(
            {"_id" : ObjectId(id)}
        )

if __name__ == "__main__":
    #Declare a mongo helper
    mongo_helper = MongoHelper()
    
    print("\n--- Record hours ---\n")

    #create a menu to insert entries in the database (or more specifically, the collection)
    choice = ""

    #Have a list to hold json documents
    entries = []

    while choice != 'q':
        #declare a dictionary object to be our Json file
        json_doc = ObjDict()

        print("Enter one of the options listed below.\n")
        print("[1]Enter 1 to enter hours")
        print("[F]Enter f finish entering hours")
        print("[2]Enter 2 to retrieve all entries")
        print("[3]Enter 3 to retrieve entries with a specific name and hours")
        print("[4]Enter 4 to update an existing entry")
        print("[5]Enter 5 to delete an entry")
        print("[q]Enter q to quit the program\n")
        
        choice = input("What would you like to do? \n")

        if choice == '1':
            json_doc['name'] = input("Enter name: ")
            json_doc['hours'] = input("Enter hours: ")
            json_doc['submissionTime'] = datetime.now()
            
            #tester
            print(json_doc)

            #add entry to the list of entries
            entries.append(json_doc)

            print("\nAdd more entries or enter F to submit times")


        elif choice == 'f':
            print("Entries are being submitted.")
            # if json list is holding one element, use insert one
            # otherwise, insert_many

            if(len(entries) == 1):
                mongo_helper.insertOneEntry(entries[0])
            else:
                mongo_helper.insertManyEntries(entries)

        elif choice == '2':
            mongo_helper.retrieveAllEntries()

        
        elif choice == '3':
            name = input("What name are you looking for? ")
            hours = input("How many hours? ")
            mongo_helper.retrieveEntryWithFilter(name, hours)

        elif choice == '4':
            mongo_id = input("What is the entry's ID? ")
            updatedHours = input("What are the updated hours? ")

            mongo_helper.updateOneEntry(mongo_id, updatedHours)
        
        elif choice == '5':
            mongo_id = input("What is the entry's ID? ")

            mongo_helper.deleteOneEntry(mongo_id)
            
        elif choice == 'q':
            print("Bye")

        else:
            print("The entered option is not valid")

    
    
    
    '''json_doc = ObjDict()
    
    json_doc['name'] = input("enter name: \n")
    json_doc['hours'] = input("enter hours: \n")
    json_doc['subTime'] = datetime.now()


    print("\n Json file: \n")
    print(json_doc)'''
