from datetime import datetime
import os
from pymongo import MongoClient

def insert_router_info(router_ip, router_data):

    mongo_uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME")
    interface = os.environ.get("INTERFACE_COLLECTION")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    routers = db[interface]

    router_data = routers.insert_one({
        "router_ip": router_ip,
        "timestamp": datetime.now(),
        "interfaces": router_data
    })

if __name__=='__main__':
    pass