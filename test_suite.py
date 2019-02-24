import utils_nosql
from constants import *
import unittest
import ast
import requests

url = 'http://localhost:7050/'

class TestScenarios(unittest.TestCase):

    def test_order_save(self):
        print('****RUNNING ORDER SAVE')
        params = {'command':'order_dets_save','params':{'menu':'a_menu','items':{'Veg Triple Rice (Rs.55)':2}}}
        req = requests.post(url,json = params)
        response = req.json()

        self.assertEqual(response['order_id'],1)

    def test_order_dets(self):
        print('****RUNNIG DETSD')

        params = {'command': 'order_dets', 'params': {'order_id':1}}
        req = requests.post(url, json=params)
        response = req.json()

        self.assertEqual(response[ORDER_ID_VAR], 1)
        self.assertEqual(response[NAME_VAR],'')
        self.assertEqual(response[INITIAL_COST_VAR],110)
