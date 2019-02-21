import utils_nosql
from constants import *
import unittest
import ast
import requests

url = 'http://0.0.0.0:7050/'

class TestScenarios(unittest.TestCase):

    def test_add_menu(self):
        params = {'command':'a_menu'}
        req = requests.post(url,json = params)
        response = req.json()

        self.assertEqual(response[ITEMS_VAR][0],'dewf')
