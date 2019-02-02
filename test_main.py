import unittest, requests
from main import app, customers


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_sort(self):
        customer_ages_sorted = sorted(customers, key=lambda c: (c['age'] is None, c['age'])) # Sort ascending with None values at end
        response = requests.get('http://localhost:5000/api/?sort=age[asc]').json()
        self.assertEqual(response, customer_ages_sorted)

    def test_filter(self):
        filtered_customers = [c for c in customers if 'ronald' in c['first_name'].lower()]
        response = requests.get('http://localhost:5000/api/?first_name=ronald').json()
        self.assertEqual(response, filtered_customers)

if __name__ == "__main__":
    unittest.main()