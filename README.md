# Pecan

Pecan is toy web application for browsing customer data.

## Installation

Pecan is built using Python 3. You will need to install the Flask framework and Flask-RESTful:

```
pip3 install flask
pip install flask-restful
```

## Starting the app

Run Pecan like this:

```
FLASK_APP=main.py flask run
```
Or run in debug mode using:
```
python main.py
```
You can then access the web front end at [http://localhost:5000/]() and the API endpoint at [http://localhost:5000/api](). 

## Usage

Supported URL query arguments:


String fields containing all or part of a search term can be found using the syntax:
```
/api/?<field>=<value>
```
Numerical fields can be searched using the syntax:
```
/api/?<field>[operator]=<value>
```
Supported operators are 'eq', 'lte' and 'gte' for equal, less than or equal to and greater than or equal to respectively.