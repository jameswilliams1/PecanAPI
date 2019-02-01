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
http://127.0.0.1:5000/api/?<field>=<value>
```
Numerical fields can be searched using the syntax:
```
http://127.0.0.1:5000/api/?<field>[operator]=<value>
```
Supported operators are 'eq', 'lte' and 'gte' for equal, less than or equal to and greater than or equal to respectively.

Any number of filters can be used simultaneously by chainng them with '&', such as:
```
http://127.0.0.1:5000/api/?name=Joe&age[gte]=25
```
Search results can be sorted using the syntax:
```
http://127.0.0.1:5000/api/?sort=<field>[direction]
```
Where supported directions are 'asc' and 'desc' for ascending and descending respectively. Sorting works for both string and numerical fields, sorting alphabetically or numerically as expected, with missing values appearing at the end.

## Examples

Show all customers aged 30-50 (inclusive) who have an income greater than 30000 and work in a bank, sorting the results by age (ascending):
```
http://127.0.0.1:5000/api/?age[gte]=30&age[lte]=50&income[gte]=30000&company=bank&sort=age[asc]
```