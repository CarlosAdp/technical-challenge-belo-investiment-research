import os

import ptax_client


client = ptax_client.PTAXClient()


def test_config_file():
    assert os.path.exists(client._configuration_file), \
            'Config file does not exist'
    assert client.configuration, 'Confinguration is empty'
