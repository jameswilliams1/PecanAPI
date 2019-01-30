import json

from flask import Flask, jsonify, request
app = Flask(__name__)

customers = json.load(open('customers.json', 'r'))


@app.route("/")
def get_customers():
    if request.args.get('gender'):
        filtered_customers = [c for c in customers if c['gender'] == request.args['gender']]
    else:
        filtered_customers = customers
    return jsonify(filtered_customers)

