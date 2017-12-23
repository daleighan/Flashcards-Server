from flask import Flask, request, abort, jsonify
import dynamo_info
from flask_dynamo import Dynamo
from boto3.dynamodb.conditions import Key, Attr
import os

app = Flask(__name__)

app.config["DYNAMO_TABLES"] = [
    {
         "TableName":"Flashcards",
         "KeySchema":[dict(AttributeName="front+name", KeyType="HASH")],
         "AttributeDefinitions":[dict(AttributeName="front+name", AttributeType="S")],
         "ProvisionedThroughput":dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    }
]

dynamo = Dynamo(app)

@app.route("/")
def slash():
    return "something else will be here"

# to send to this route: /api/all_by_user/?username={username}
@app.route("/api/all_by_user/")
def get_all_by_user():
    response = dynamo.tables["Flashcards"].scan(
        FilterExpression=Attr('username').eq(request.args["username"])
    )
    return jsonify(response)

@app.route("/api/add_card", methods=["POST"])
def add_card():
    if not request.json:
        abort(400)
    dynamo.tables["Flashcards"].put_item(Item={
        "username": request.json["username"],
        "category": request.json["category"],
        "front+name": request.json["front"] + "-" + request.json["username"],
        "username": request.json["username"],
        "front": request.json["front"],
        "back": request.json["back"],
    })
    return jsonify(request.json)

@app.route("/api/delete_one", methods=["POST"])
def delete_card():
    if not request.json:
        abort(400)
    dynamo.tables["Flashcards"].delete_item(
        Key = {
            "front+name": request.json["front"] + "-" + request.json["username"]
        }
    )
    return jsonify({ "card deleted" : request.json["front"] })

@app.route("/api/fetch_all")
def fetch_all():
    response = dynamo.tables["Flashcards"].scan()
    return jsonify(response)

if __name__ == "__main__":
    with app.app_context():
        dynamo.create_all()
    app.run(debug=True, host="0.0.0.0", port=80)
