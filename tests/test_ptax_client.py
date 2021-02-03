from datetime import date, timedelta
import unittest

from flask_app import ptax_client


client = ptax_client.PTAXClient()


class PTAXUnitTest(unittest.TestCase):
    client: ptax_client.PTAXClient

    def setUp(self: 'PTAXUnitTest') -> None:
        self.client = ptax_client.PTAXClient()

    def tearDown(self: 'PTAXUnitTest') -> None:
        self.client.close()

    def test_non_empty(self: 'PTAXUnitTest'):
        self.assertFalse(
            expr=self.client.get(
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 20),
                currency='USD'
            ).empty,
            msg='Should be a non-empty pandas data frame'
        )

    def test_empty(self: 'PTAXUnitTest'):
        self.assertTrue(
            expr=self.client.get(
                start_date=date(2021, 1, 1),
                end_date=date(2021, 1, 2),
                currency='USD'
            ).empty,
            msg='Should be an empty pandas data frame'
        )

    def test_100_days_interval(self: 'PTAXUnitTest'):
        start_date = date(2020, 1, 1)
        end_date = start_date + timedelta(days=100)

        self.assertFalse(
            expr=self.client.get(
                start_date=start_date,
                end_date=end_date,
                currency='USD'
            ).empty,
            msg='Should be a non-empty pandas data frame'
        )

    def test_200_days_interval(self: 'PTAXUnitTest'):
        start_date = date(2020, 1, 1)
        end_date = start_date + timedelta(days=200)

        self.assertFalse(
            expr=self.client.get(
                start_date=start_date,
                end_date=end_date,
                currency='USD'
            ).empty,
            msg='Should be a non-empty pandas data frame'
        )

    def test_500_days_interval(self: 'PTAXUnitTest'):
        start_date = date(2020, 1, 1)
        end_date = start_date + timedelta(days=500)

        self.assertFalse(
            expr=self.client.get(
                start_date=start_date,
                end_date=end_date,
                currency='USD'
            ).empty,
            msg='Should be a non-empty pandas data frame'
        )

    def test_invalid_interval(self: 'PTAXUnitTest'):
        exception = ptax_client.exceptions.InvalidIntervalError
        start_date = date(2021, 1, 1)
        end_date = start_date - timedelta(days=100)

        self.assertRaises(
            exception,
            self.client.get,
            start_date,
            end_date,
            'USD',
        )


if __name__ == '__main__':
    unittest.main()
