from flask import json
from unittest import TestCase
import unittest
from delivery_calculator import app


class TestView(unittest.TestCase):

    # testing the given example, where delivery_fee should be 710, the next tests are based on this one too
    def test_given_example(self):
        tester = app.test_client()
        response = tester.post('/',
                               data=json.dumps(
                                   {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4,
                                    "time": "2021-10-12T13:00:00Z"}),
                               content_type='application/json',
                               )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['delivery_fee'], 710)

    # as now cart value 10e and surcharge is 0, so delivery fee should be 710 - 210 = 500
    def test_cart_value(self):
        tester = app.test_client()
        response = tester.post('/',
                               data=json.dumps(
                                   {"cart_value": 1000, "delivery_distance": 2235, "number_of_items": 4,
                                    "time": "2021-10-12T13:00:00Z"}),
                               content_type='application/json',
                               )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['delivery_fee'], 500)

    # distance is now only 1000m (nothing to add for every 500m), so delivery fee 710 - 300 = 410
    def test_distance(self):
        tester = app.test_client()
        response = tester.post('/',
                               data=json.dumps(
                                   {"cart_value": 790, "delivery_distance": 1000, "number_of_items": 4,
                                    "time": "2021-10-12T13:00:00Z"}),
                               content_type='application/json',
                               )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['delivery_fee'], 410)

    # number of products increased, so 0.5 will be added for each, delivery fee is 710 + (6-4)*50 = 810
    def test_number_of_items(self):
        tester = app.test_client()
        response = tester.post('/',
                               data=json.dumps(
                                   {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 6,
                                    "time": "2021-10-12T13:00:00Z"}),
                               content_type='application/json',
                               )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['delivery_fee'], 810)

    # delivery fee would be here 1000-190 + 200 + 7*100 = 1710, but it can never be more than 1500
    def test_max_delivery_fee(self):
        tester = app.test_client()
        response = tester.post('/',
                               data=json.dumps(
                                   {"cart_value": 190, "delivery_distance": 4235, "number_of_items": 4,
                                    "time": "2021-10-12T13:00:00Z"}),
                               content_type='application/json',
                               )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['delivery_fee'], 1500)

    # when cart value is 10000 or more, delivery fee is 0
    def test_zero_fee(self):
        tester = app.test_client()
        response = tester.post('/',
                               data=json.dumps(
                                   {"cart_value": 10000, "delivery_distance": 2235, "number_of_items": 4,
                                    "time": "2021-10-12T13:00:00Z"}),
                               content_type='application/json',
                               )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['delivery_fee'], 0)

    # value of final delivery fee is multiplied by 1.1 during the Friday rush, so delivery fee is 710 * 1.1 = 781
    def test_rush_time(self):
        tester = app.test_client()
        response = tester.post('/',
                               data=json.dumps(
                                   {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4,
                                    "time": "2021-10-15T15:00:00Z"}),
                               content_type='application/json',
                               )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['delivery_fee'], 781)


if __name__ == '__main__':
    unittest.main()
