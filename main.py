import json

from flask import Flask, request, Response
from pymongo import MongoClient

app = Flask(__name__)
mongo = MongoClient(host='localhost', port=27017)
db = mongo.users


@app.route('/users/', methods=['GET'])
def get_some_users():
    data = list(db.users.find())
    if data:
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(response=json.dumps(data),
                        status=200,
                        mimetype='application/json'
                        )
    return Response(response=json.dumps({'message': 'Users list is empty'}),
                    status=500,
                    mimetype='application/json'
                    )


@app.route('/users/', methods=['POST'])
def create_user():
    user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "username": request.form["username"]
    }
    if db.users.count_documents({'username': user['username']}):
        return Response(response=json.dumps(
            {'message': 'This username already exists'}),
            status=409,
            mimetype='application/json'
        )
    db_response = db.users.insert_one(user)
    return Response(response=json.dumps(
        {"message": "User created",
         "id": f"{db_response.inserted_id}",
         "first_name": user['first_name'],
         "last_name": user['last_name'],
         "username": user['username']
         }),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(debug=True, port=5050)
