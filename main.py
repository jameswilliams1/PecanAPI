import json, datetime
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
customers = json.load(open('customers.json', 'r'))


class Customer(Resource):
    """Finds one customer by their ID"""
    def get(self, id_number):
        customer_by_id = list(filter(lambda c: c['id'] == id_number, customers))
        if not customer_by_id:
            return "No customer with id {}".format(id_number), 400
        return jsonify(customer_by_id)


class Customers(Resource):
    """Finds all customers matching a filter"""
    def get(self):
        filtered_customers = customers
        search_arguments = request.args
        for key in search_arguments:
            if key == 'gender' or key == 'has_children' or key == 'marital_status' or key == 'title': # Must be an exact match (case-insensitive)
                filtered_customers = list(filter(lambda c: str(c[key]).lower() == str(search_arguments[key]).lower(), filtered_customers))
            elif key == 'company' or key == 'first_name' or key == 'last_name' or key == 'profession': # Contains partial match (case-insensitive)
                filtered_customers = list(filter(lambda c: str(search_arguments[key]).lower() in str(c[key]).lower() , filtered_customers))
            elif key == 'age[gte]' or key == 'income[gte]' or key == 'wealth[gte]': # Customer value >= search value
                key_sub = key.split('[', 1)[0]
                print(key_sub)
                print(search_arguments[key])
                filtered_customers =  list(filter(lambda c: float(c[key_sub]) >= float(search_arguments[key]), filtered_customers))
            else:
                return 'Bad request: {} is not a recognised filter.'.format(key), 400

        return jsonify(filtered_customers)



api.add_resource(Customer, "/customers/<int:id_number>") # Quickly find a customer by id number
api.add_resource(Customers, "/customers/") # Search all customers

if __name__ == "__main__":
    app.run(debug=True)