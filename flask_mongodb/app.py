import json

from flask import Flask, Response
from pymongo import MongoClient
from bson import json_util
from flask import Flask, request, jsonify, render_template
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)




app = Flask(__name__, static_folder='static', template_folder='templates')
client = MongoClient('mongo', 27017)
db = client['flask_mongodb']
collection = db['users']


@app.route('/add/<name>/<password>', methods=['POST'])
def add(name=None, password=18):
    result = collection.insert_one({'name': name, 'password': password})

    otv = JSONEncoder().encode(result.inserted_id)
    return {'j': otv}


@app.route('/all')
def all():

    result = collection.find()
    return json_util.dumps(result)


@app.route('/find/<name>')
def find(name=None):
    result = collection.find({'name': name})
    return json_util.dumps(result)


@app.route('/show_reg_users', methods=['GET'])
def show_reg_users():
    users = list(collection.find({}, {"_id": 0}))  # Убираем поле _id для удобства
    return render_template('users.html',users=users)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
