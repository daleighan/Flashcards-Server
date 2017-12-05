from flask import Flask, request, abort, jsonify
import dynamo_info
from flask_dynamo import Dynamo
import os

app = Flask(__name__)

app.config['DYNAMO_TABLES'] = [
    {
         "TableName":"Flashcards",
         "KeySchema":[dict(AttributeName="id", KeyType='HASH')],
         "AttributeDefinitions":[dict(AttributeName="username", AttributeType="S"), dict(AttributeName="category", AttributeType="S"), dict(AttributeName="front", type="S"), dict(AttributeName="back", type="S")],
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
    print('eyo')
    return "Card Posted"

if __name__ == "__main__":
    with app.app_context():
        dynamo.create_all()
    app.run()
