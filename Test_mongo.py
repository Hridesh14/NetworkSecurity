import urllib.parse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# 1. Separate your credentials
user = "maithanihridesh9012_db_user"
password = "Hridesh90@12"

# 2. Escape them properly (this handles the RFC 3986 requirement)
escaped_user = urllib.parse.quote_plus(user)
escaped_pass = urllib.parse.quote_plus(password)

# 3. Reconstruct the URI
uri = f"mongodb+srv://{escaped_user}:{escaped_pass}@cluster0.dpxf1qc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting: {e}")