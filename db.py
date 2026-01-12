import pymongo
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

# Configuration from your constants
MONGO_DB_URL = os.getenv('MONGO_DB_URL')
DB_NAME = "HrideshNetworkAI"
COLLECTION_NAME = "NetworkData"

try:
    client = pymongo.MongoClient(MONGO_DB_URL)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # 1. Check if we can even connect
    print(f"Connected to MongoDB: {client.server_info()['version']}")
    
    # 2. Check document count
    count = collection.count_documents({})
    print(f"Documents found in {DB_NAME}.{COLLECTION_NAME}: {count}")
    
    # 3. Test DataFrame conversion
    df = pd.DataFrame(list(collection.find()))
    print(f"DataFrame Shape: {df.shape}")

except Exception as e:
    print(f"Error: {e}")