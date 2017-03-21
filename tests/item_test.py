import unittest
import json
from keanu.app import flask_app


class TestItemRoute(unittest.TestCase):

    test_item = '{"name": "testItem101", "description": "this is a description", "imageURL": "https://example.com", ' \
               '"price": 33.95, "calories": 500, "category": "Starter", "tags": ["asdf", "sdfsdf", "sdfs"]}'

    def setUp(self):
        """
        Setup app for testing
        :return:
        """
        self.app = flask_app.test_client()
        self.app.testing = True

    def tearDown(self):
        """
        Remove app after testing
        :return:
        """
        self.app.delete()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_get_all_items(self):
        result = self.app.get('/item')
        json_data = json.loads(result.data)
        self.assertTrue(len(json_data['data']['items']) > 1, 'no items in db')

    def test_get_item_by_id(self):
        result = self.app.get('/item/id/58be0265f188127b8fd2af52')
        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['item'] is not None, 'no item by id found')

    def test_get_item_by_category(self):
        result = self.app.get('/item/category/Starter')
        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['items'] is not None, 'no item by id found')

    def test_admin_add_item(self):
        data= '{"name": "testItem101",	"description": "this is a description",	"imageURL": "https://example.com",' \
              '	"price": 33.95,	"calories": 500, "category": "Starter", "tags": ["asdf", "sdfsdf", "sdfs"]}'
        # loin as admin and get admin token
        login_result = self.app.post('/login', headers={'username': 'aaron', 'password': 'password'})
        admin_token = json.loads(login_result.data)['data']['token']
        # add item as admin
        result = self.app.post(
            '/admin/item/add',
            headers={'Content-Type': 'application/json', 'token': admin_token},
            data=data
        )

        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['item'] is not None, 'item not added')