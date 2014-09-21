from pymongo import MongoClient
def build_mongo_client(app):
    if app.config["DEBUG"]:
        # We might not be running on the sever, so explicitly supply an ip
        # address
        client = MongoClient(app.config["HOST_IP"])
    else:
        # We are running on the server, connect via localhost
        client= MongoClient()
    username = app.config["MONGO_USERNAME"]
    password = app.config["MONGO_PASSWORD"]
    client.admin.authenticate(username,password)
    return client
