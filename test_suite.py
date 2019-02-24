import utils_nosql
from constants import *
import unittest
import ast
import requests

url = 'http://localhost:7050/'

class TestScenarios(unittest.TestCase):
    @unittest.skip
    def test_order_save(self):
        print('****RUNNING ORDER SAVE')
        params = {'command':'order_dets_save','params':{'menu':'a_menu','items':{'Veg Triple Rice (Rs 55)':2}}}
        req = requests.post(url,json = params)
        response = req.json()

        self.assertEqual(response['order_id'],1)

    def test_order_dets(self):
        print('****RUNNIG DETSD')
        params = {'command': 'order_dets_save', 'params': {'menu': 'a_menu', 'items': {'Veg Triple Rice (Rs 55)': 2}}}
        req = requests.post(url, json=params)

        params = {'command': 'order_dets_saved_request', 'params': {'order_id':2}}
        req = requests.post(url, json=params)
        response = req.json()

        self.assertEqual(response[ITEMS_VAR], {'Veg Triple Rice (Rs 55)': 2})

    def test_order_prices(self):
        print('****RUNNIG prices')
        params = {'command': 'order_dets_save', 'params': {'menu': 'a_menu', 'items': {'Veg Triple Rice (Rs 55)': 2}}}
        req = requests.post(url, json=params)

        params = {'command': 'order_prices', 'params': {'order_id':3}}
        req = requests.post(url, json=params)
        response = req.json()

        self.assertEqual(response[ITEMS_VAR], {'Veg Triple Rice (Rs 55)': 55})

    def test_cal_prices(self):
        print('****RUNNIG cal prices')
        params = {'command': 'order_dets_save', 'params': {'menu': 'a_menu', 'items': {'Veg Triple Rice (Rs 55)': 2}}}
        req = requests.post(url, json=params)

        params = {'command': 'calculated_prices', 'params': {'order_id': 1}}
        req = requests.post(url, json=params)
        response = req.json()

        self.assertEqual(response[ITEMS_VAR], [110,20,10,140])
