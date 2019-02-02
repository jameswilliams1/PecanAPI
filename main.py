import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
customers = json.load(open('customers.json', 'r'))


def number_filter(operator, num1, num2):
    try:
        if operator.lower() == 'eq':
            return num1 == num2
        elif operator.lower() == 'gte':
            return num1 >= num2
        elif operator.lower() =='lte':
            return num1 <= num2
    except TypeError: # Catch None values
        return False


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
            elif 'age[' in key or 'income[' in key or 'wealth[' in key: # Filters numerical values using supplied operator
                key_sub, operator = key.split('[', 1)
                operator = operator[:-1]
                if key_sub == 'age' or key_sub == 'income' or key_sub == 'wealth':
                    pass
                else:
                    return 'Bad request: {} is not a valid field.'.format(key_sub), 400
                try:
                    compare_number = float(search_arguments[key])
                except ValueError:
                    return 'Bad request: {} is not a number.'.format(search_arguments[key]), 400
                filtered_customers =  [c for c in filtered_customers if number_filter(operator, c[key_sub], compare_number)]
            elif key == 'sort': # Sorts either direction with null values at the end
                sort_value, direction = search_arguments['sort'].split('[', 1)
                direction = direction[:-1]
                is_desc = False
                accepted_values = ['age', 'income', 'wealth', 'first_name', 'last_name', 'gender', 'marital_status', 'title', 'has_children']
                if any(term == sort_value for term in accepted_values):
                    pass
                else:
                    return 'Bad request: {} is not a valid field.'.format(sort_value), 400
                if direction == 'asc':
                    pass
                elif direction == 'desc':
                    is_desc = True
                else:
                    return 'Bad request: {}. Sort direction must be asc or desc.'.format(search_arguments[key]), 400
                no_value = list(filter(lambda c: c[sort_value] == None, filtered_customers))
                filtered_customers = list(filter(lambda c: c[sort_value] != None, filtered_customers))
                filtered_customers = sorted(filtered_customers, reverse=is_desc, key=lambda c: c[sort_value])
                filtered_customers = filtered_customers + no_value
            else:
                return 'Bad request: {} is not a recognised filter.'.format(key), 400
        return jsonify(filtered_customers)


api.add_resource(Customer, "/api/<int:id_number>") # Quickly find a customer by id number
api.add_resource(Customers, "/api/") # Search all customers
@app.route('/')
def home():
    return "<H1>Pecan API</H1>"

if __name__ == "__main__":
    app.run(debug=True)