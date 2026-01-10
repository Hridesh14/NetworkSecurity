import os
import json
import sys
import certifi
import pandas as pd 
import numpy as np
import pymongo
import urllib.parse
from dotenv import load_dotenv

# Import custom logger and exception
from Networksecurity.logging.logger import logging
from Networksecurity.Exception.Exception import NetworkSecurityException

# Load environment variables
load_dotenv()

# Get the link from .env
MOMGO_DB_LINK = os.getenv('MONGO_DB_URL')
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        pass
    
    def csv_to_json_Conv(self, File_path):
        """
        Converts CSV data into a list of dictionaries (JSON format) 
        that MongoDB can accept.
        """
        try:
            # 1. Read the CSV file
            data = pd.read_csv(File_path)
            data.reset_index(drop=True, inplace=True)
            
            # 2. Convert DataFrame rows into a list of dictionaries
            # 'orient=records' ensures each row is a separate document
            records = list(json.loads(data.to_json(orient='records')))
            
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_momgo_record(self, record, database, collection):
        """
        Inserts the list of records into the specified MongoDB collection.
        """
        try:
            # Check if record list is empty to prevent MongoDB error
            if not record or len(record) == 0:
                print("No records found to insert.")
                return 0

            # 3. Initialize MongoClient with SSL bypass for Mobile Hotspots
            # Added tlsAllowInvalidCertificates to fix the 'tlsv1 alert internal error'
            self.mongo_client = pymongo.MongoClient(
                MOMGO_DB_LINK,
                tlsCAFile=ca,
                tlsAllowInvalidCertificates=True, 
                serverSelectionTimeoutMS=5000
            )

            self.db = self.mongo_client[database]
            self.coll = self.db[collection]

            # 4. Perform the bulk insertion
            results = self.coll.insert_many(record)
            
            return len(results.inserted_ids)
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    # Use 'r' before the string to fix the SyntaxWarning for \p
    FILE_path = r'Network_Data\phisingData.csv'
    DATABASE = 'HrideshNetworkAI'
    Collection = 'NetworkData'
    
    networkobj = NetworkDataExtract()
    
    try:
        print("Starting data conversion...")
        record = networkobj.csv_to_json_Conv(File_path=FILE_path)
        print(f"Total records prepared from CSV: {len(record)}")
        
        print("Connecting to MongoDB and pushing data...")
        no_of_record = networkobj.insert_momgo_record(record, DATABASE, Collection)
        
        print(f"Process Completed! Successfully inserted {no_of_record} records.")
        
    except Exception as e:
        # This will print the detailed error message from your Exception class
        print(e)