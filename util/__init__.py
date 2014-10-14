from pymongo import MongoClient
def build_mongo_client(app):
    client = MongoClient(app.config["HOST_IP"])
    username = app.config["MONGO_USERNAME"]
    password = app.config["MONGO_PASSWORD"]
    client.admin.authenticate(username,password)
    return client
