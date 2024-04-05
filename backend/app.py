from flask import Flask, render_template
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)
db = TinyDB('db.json')
#command_table = db.table('logs')

@app.route('/')
def main():
	return render_template('index.html')



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)



