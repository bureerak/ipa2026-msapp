import os
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")
interface = os.environ.get("INTERFACE_COLLECTION")

client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routers"]
myinterface = mydb[interface]

app = Flask(__name__)
data = []


@app.route("/")
def main():
    data.clear()
    for doc in mycol.find():
        data.append(doc)
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        data.append({"ip": ip, "username": username, "password": password})
        mycol.insert_one({"ip": ip, "username": username, "password": password})
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete_comment():
    try:
        ip = request.form.get("ip")
        username = request.form.get("username")
        mycol.delete_one({"ip": ip, "username": username})
    except Exception:
        print("delete failed")
    return redirect(url_for("main"))


@app.route("/route/<ip>", methods=["GET"])
def show_route(ip):
    data = myinterface.find({"router_ip": ip}).sort({"timestamp": -1}).limit(5)
    return render_template("route.html", data=list(data))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
