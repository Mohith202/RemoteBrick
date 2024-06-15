from pymongo import MongoClient, server_api
from urllib.parse import quote_plus

# Example username, password, and database name
username = "20eg103319"
password = "Saroj@2002"  # Replace with your actual password


# Encode the password for the MongoDB URI
encoded_password = quote_plus(password)

# Construct the MongoDB URI
uri = f"mongodb+srv://{username}:{encoded_password}@mydata.bkwkloc.mongodb.net/?retryWrites=true&w=majority&appName=MyData"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=server_api.ServerApi('1'))

# Select the database
db = client.user_database
