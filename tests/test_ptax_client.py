import os
from datetime import date

import ptax_client


client = ptax_client.PTAXClient()


def test_config_file_exists():
    assert os.path.exists(client._config_file), \
            'Config file does not exist'


def test_config_not_empty():
    assert client.config, 'Configuration is empty'


def test_not_empty():
    assert not client.get(
        initial_date=date(2021, 1, 1),
        final_date=date(2021, 1, 20),
        currency='USD'
    ).empty, 'Should be a non-empty pandas data frame'


def test_no_data():
    assert client.get(
        initial_date=date(2021, 1, 1),
        final_date=date(2021, 1, 2),
        currency='USD'
    ).empty, 'Should be an empty pandas data frame'
