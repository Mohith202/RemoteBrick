from pymongo import MongoClient, server_api
from urllib.parse import quote_plus


username = "#####"
password = "#####"  # Replace with your actual password

encoded_password = quote_plus(password)

# Construct the MongoDB URI
uri = f"mongodb+srv://{username}:{encoded_password}@mydata.bkwkloc.mongodb.net/?retryWrites=true&w=majority&appName=MyData"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=server_api.ServerApi('1'))


db = client.user_database
