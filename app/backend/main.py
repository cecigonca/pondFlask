import time
from flask import Flask
from tinydb import TinyDB, Query


app = Flask(__name__)
db = TinyDB('db.json')

comando= "ande gora"


db.insert({'command':comando, 'time': time.time() })


@app.route("/")
def hello_world():
    return db.all()
