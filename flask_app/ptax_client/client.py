__all__ = ['PTAXClient']

from datetime import date
import os
from io import StringIO

from lxml import etree
import yaml
import requests
import pandas
from open_close_mixin import OpenCloseMixin

from .exceptions import InvertedIntervalError

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.yml')


class PTAXClient(OpenCloseMixin):
    '''Define a client for carrying scraping requests to BACEN's endpoint.'''
    config = {}

    def __init__(self: 'PTAXClient') -> None:
        '''Please refer to this class documentation.'''
        self.open()

    def open(self: 'PTAXClient') -> None:
        '''Load the configuration file into the `config` attribute.'''
        with open(CONFIG_FILE, 'r') as fd:
            self.config.update(yaml.safe_load(fd))

        super().open()

    def get(
        self: 'PTAXClient',
        start_date: date,
        end_date: date,
        currency: str,
    ) -> pandas.DataFrame:
        '''Return a data frame containing PTAX data.

        :param start_date: start date of the desired period
        :type start_date: `datetime.date`
        :param end_date: end date of the desired period
        :type end_date: `datetime.date`
        :param currency: currency code according to ISO 4217
        :type currency: str
        :return: a data frame containing PTAX data
        :rtype: `pandas.DataFrame`
        '''
        config = self.config
        base_url = config['request']['base_url']
        params = config['request']['params'].copy()

        currencies_ids = config['currencies_ids']
        date_format = config['date_format']

        params.update({
            'ChkMoeda': currencies_ids[currency],
            'DATAINI': start_date.strftime(date_format),
            'DATAFIM': end_date.strftime(date_format)
        })

        response = requests.get(url=base_url, params=params)

        try:
            content = StringIO(response.text)
            return pandas.read_csv(
                content,
                delimiter=config['csv']['delimiter'],
                names=config['csv']['columns'],
                usecols=config['csv']['desired_columns']
            )
        except pandas.errors.ParserError:
            dom = etree.fromstring(response.text, parser=etree.HTMLParser())
            error = dom.xpath(config['error']['xpath'])

            if config['error']['msgs']['no_data'] in error:
                return pandas.DataFrame(
                    columns=config['csv']['desired_columns']
                )

            if config['error']['msgs']['inverted_interval'] in error:
                raise InvertedIntervalError('Parameters: (%s, %s, %s)' % (
                        start_date, end_date, currency
                ))
