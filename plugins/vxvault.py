import datetime
import re

from yapsy.IPlugin import IPlugin


class PluginOne(IPlugin):
    NAME = "vxvault"
    DIRECTION = "outbound"
    URLS = ['http://vxvault.net/URL_List.php']

    def get_URLs(self):
        return self.URLS

    def get_direction(self):
        return self.DIRECTION

    def get_name(self):
        return self.NAME

    def process_data(self, source, response):
        current_date = str(datetime.date.today())
        data = []
        for line in response.splitlines():
            if line.startswith('http'):
                data.append({'indicator': line, 'indicator_type': "URL", 'indicator_direction': self.DIRECTION,
                             'source_name': self.NAME, 'source': source, 'date': current_date})
        return data
