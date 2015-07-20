import datetime
import bs4
import re

from yapsy.IPlugin import IPlugin


class PluginOne(IPlugin):
    NAME = "urlquery"
    DIRECTION = "outbound"
    URLS = ['https://urlquery.net/']

    def get_URLs(self):
        return self.URLS

    def get_direction(self):
        return self.DIRECTION

    def get_name(self):
        return self.NAME

    def process_data(self, source, response):
        current_date = str(datetime.date.today())
        data = []
        soup = bs4.BeautifulSoup(response)
        for t in soup.find_all("table", class_="test"):
            for a in t.find_all("a"):
                indicator = 'http://' + re.sub('&amp;', '&', a.text)
                data.append({'indicator': indicator, 'indicator_type': "URL", 'indicator_direction': self.DIRECTION,
                             'source_name': self.NAME, 'source': source, 'date': current_date})
        return data
