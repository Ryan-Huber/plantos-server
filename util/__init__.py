from pymongo import MongoClient
def build_mongo_client(app):
    client = MongoClient(app.config["HOST_IP"])
    username = app.config["MONGO_USERNAME"]
    password = app.config["MONGO_PASSWORD"]
    try:
        client.admin.authenticate(username,password)
    except:
        print "Failed to authenticate to database. Either the database does not \
require authentication or the login information in instance application.cfg is \
incorrect"
    return client
