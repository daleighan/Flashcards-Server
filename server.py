from flask import Flask, request, abort, jsonify
import dynamo_info
from flask_dynamo import Dynamo
import os

app = Flask(__name__)

app.config['DYNAMO_TABLES'] = [
    {
         "TableName":"Flashcards",
         "KeySchema":[dict(AttributeName="id", KeyType="HASH")],
         "AttributeDefinitions":[dict(AttributeName="id", AttributeType="N") ],
         "ProvisionedThroughput":dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    }
]

dynamo = Dynamo(app)

@app.route("/")
def hello_world():
    return "Hello World"

@app.route("/api/add_card", methods=["POST"])
def add_card():
    if not request.json:
        abort(400)
    print(request.json)
    dynamo.tables["Flashcards"].put_item(Item={
        "id": request.json["id"],
        "username": request.json["username"],
        "category": request.json["category"],
        "front": request.json["front"],
        "back": request.json["back"]
    })
    return "Card Posted"

if __name__ == "__main__":
    with app.app_context():
        dynamo.create_all()
    app.run()
