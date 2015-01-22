# -*- coding: iso-8859-15 -*-
"""Simple FunkLoad test

"""
import unittest
import random

from funkload.FunkLoadTestCase import FunkLoadTestCase

PAGES = (('Homepage', ''),
         ('Inbox', 'stresstest/inboxview'),
         )


COUNTRIES = ['at'] #,'be','bg','hr','cy','cz','dk','ee','fi','fr','de','gr','hu','is','ie','it','lv','lt','lu','mt','nl','pl','pt','ro','sk','sl','es','se','uk']

CRF_CODES = ['1A1'] #, '1A1a', '1A1b', '1A1c', '1A2', '1A2a', '1A2b', '1A2c', '1A2d', '1A2e', '1A2f', '1A2g', '1A3', '1A3a', '1A3b', '1A3c', '1A3d', '1A3e', '1A4', '1A4a', '1A4b', '1A4c', '1A5', '1A5a', '1A5b', '1B1', '1B2a', '1B2b', '1C', '1D1', '1D1a', '1D1b', '1D2', '1D4', '1AB', '2A1', '2A2', '2A3', '2A4', '2B1', '2B2', '2B3', '2B4', '2B5', '2B6', '2B7', '2B8', '2B9', '2C1', '2C2', '2C3', '2C4', '2C5', '2C6', '2D', '2E', '2F1', '2F2', '2F3', '2F4', '2F5', '2F6', '2G', '2H', '3A', '3B', '3C', '3D1', '3D2', '3E', '3F', '3G', '3H', '3I', '4A1', '4A2', '4B1', '4B2', '4C1', '4C2', '4D1', '4D2', '4E1', '4E2', '4F1', '4F2', '4G', '4H', '5A', '5B', '5C', '5D', '5E', '5F', '6', '7']

GASES = ['CO2','CH4','N20','HFCs','PFCs','SF6','NF3']

FUEL = ['gaseous', 'liquid', 'solid', 'biomass', 'other']

PARAMETER = ['efep', 'act', 'emi', 'other']

HIGHLIGHT = ['ne', 'pgf', 'ptc', 'psi', 'recalc', 'recalc', 'unfccc', 'ur']


class Site(FunkLoadTestCase):
    """This test uses a configuration file Site.conf."""

    def get_random_country(self):
        return random.choice(COUNTRIES)

    def get_random_crf_code(self):
        return random.choice(CRF_CODES)

    def get_random_gases(self):
        number_of_gases = len(GASES)
        select = random.randint(1, number_of_gases) - 1
        return GASES[:select]

    def get_random_fuel(self):
        return random.choice(FUEL)

    def get_random_parameter(self):
        number_of_gases = len(PARAMETER)
        select = random.randint(1, number_of_gases) - 1
        return random.choice(PARAMETER)

    def get_random_highlight(self):
        number_of_gases = len(HIGHLIGHT)
        select = random.randint(1, number_of_gases) - 1
        return random.choice(HIGHLIGHT)

    def get_random_observation_data(self, number=1):
        items = []
        for i in xrange(number):
            params = [
                ["form.widgets.text", 'Example observation'],
                ["form.widgets.country:list", self.get_random_country()],
                ["form.widgets.crf_code:list", self.get_random_crf_code()],
                ["form.widgets.year", '2014'],
                ["form.widgets.gas:list", self.get_random_gases()],
                ["form.widgets.review_year", '2014'],
                ["form.widgets.fuel:list", self.get_random_fuel()],
                ["form.widgets.ms_key_catagory", 'selected'],
                ["form.widgets.eu_key_catagory", 'selected'],
                ["form.widgets.parameter:list", self.get_random_parameter()],
                ["form.widgets.highlight", self.get_random_highlight()],
                ['form.buttons.save', 'Save Observation'],
                ['form.submitted', '1'],
                ['js_enabled', '0'],
                ['cookies_enabled', ''],
            ]
            items.append(params)
        return items

    def setUp(self):
        """Setting up test."""
        self.server_url = self.conf_get('main', 'url')

    def test_app(self):
        ''' site path
        '''
        server_url = self.server_url

        self.get(self.server_url + "/login_form",
            description="Get /login_form")

        self.post(self.server_url + "/login_form",
            params=[
                ['came_from', self.server_url],
                ['form.submitted', '1'],
                ['js_enabled', '0'],
                ['cookies_enabled', ''],
                ['login_name', ''],
                ['pwd_empty', '0'],
                ['__ac_name', 'PUT HERE A VALID USERNAME'],
                ['__ac_password', 'PUT HERE A VALID USERNAME'],

                ['submit', 'Login']],
            description="Post for login a user /login_form")

        for title, page in PAGES:
            url = "/".join((server_url, page or 'index'))
            self.get(url, description='Get %s' % title)

        for params in self.get_random_observation_data(3):
            created = self.post(
                "%s/stresstest/++add++Observation" % server_url,
                params=params,
                description="Create an Observation"
            )


if __name__ in ('main', '__main__'):
    unittest.main()
