import unittest
from flask_app.app import application
import json


class FlaskAppTest(unittest.TestCase):

    def setUp(self: 'FlaskAppTest'):
        self.application = application.test_client()

    def test_home_status_code(self: 'FlaskAppTest'):
        result = self.application.get('/')
        self.assertEqual(result.status_code, 200)

    def test_home_response(self: 'FlaskAppTest'):
        result = self.application.get('/')
        self.assertListEqual(
            list(json.loads(result.data.decode()).keys()),
            ['endpoint', 'description', 'parameters', 'example']
        )

    def test_ptax_missing_parameter(self: 'FlaskAppTest'):
        result = self.application.get('/ptax_data?start_date=foo')

        self.assertIn('Required parameters', result.data.decode())

    def test_invalid_interval(self: 'FlaskAppTest'):
        result = self.application.get(
            '/ptax_data?start=01/01/2021'
            '&end=01/01/2020'
            '&currencies=USD'
        )

        self.assertIn('Invalid interval', result.data.decode())

    def test_not_registered_currency(self: 'FlaskAppTest'):
        result = self.application.get(
            '/ptax_data?start=01/01/2021'
            '&end=01/01/2020'
            '&currencies=BRL'
        )

        self.assertIn(
            'Currency BRL is not registered yet',
            result.data.decode()
        )

    def test_invalid_date(self: 'FlaskAppTest'):
        result = self.application.get(
            '/ptax_data?start=01/01/202'
            '&end=01/01/2020'
            '&currencies=USD'
        )

        self.assertIn(
            'does not match format',
            result.data.decode()
        )

    def test_content_type(self: 'FlaskAppTest'):
        result = self.application.get(
            '/ptax_data?start=01/01/2021'
            '&end=10/01/2021'
            '&currencies=USD'
        )

        self.assertEqual(
            result.headers['Content-Type'],
            'text/csv'
        )
