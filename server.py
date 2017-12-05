from flask import Flask, request, abort, jsonify
import dynamo_info
from flask_dynamo import Dynamo

app = Flask(__name__)

app.config['DYNAMO_TABLES'] = [
    {
         "TableName":"Flashcards",
         "KeySchema":[dict(AttributeName="front", KeyType="HASH")],
         "AttributeDefinitions":[dict(AttributeName="front", AttributeType="S")],
         "ProvisionedThroughput":dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    }
]

dynamo = Dynamo(app)

@app.route("/api/add_card", methods=["POST"])
def add_card():
    if not request.json:
        abort(400)
    print(request.json)
    dynamo.tables["Flashcards"].put_item(Item={
        "username": request.json["username"],
        "category": request.json["category"],
        "front": request.json["front"],
        "back": request.json["back"]
    })
    return jsonify(request.json)

@app.route("/api/fetch_all")
def fetch_all():
    response = dynamo.tables["Flashcards"].scan()
    return jsonify(response)

if __name__ == "__main__":
    with app.app_context():
        dynamo.create_all()
    app.run()
