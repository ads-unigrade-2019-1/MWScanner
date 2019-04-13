import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner import BASE_URL
from mwscanner.Discipline import Discipline
from mwscanner.Mixins import TableReaderMixin, UrlLoaderMixin


class Department(TableReaderMixin, UrlLoaderMixin):

    def __init__(self, campus, code, name, initials):
        # department attributes
        self.campus = campus
        self.code = code
        self.name = name
        self.initials = initials

        self.disciplines = []
        self.unprocessedDisciplines = []

    def getDisciplineListURL(self):
        # This method take the url of the
        # disciplines from the department code
        return BASE_URL + 'graduacao/oferta_dis.aspx?cod={}'.format(self.code)

    def buildLinkList(self):
        # This method builds the list of disciplines that belongs
        # to this departament. This list will be later used to
        # process the creation of the Discipline object.

        response = self.getFromUrl(self.getDisciplineListURL())

        if response.status_code != 200:
            return

        # Make the parse for html
        raw_html = BeautifulSoup(response.content, 'html.parser')
        table_data = self.readDatatableTableFromHTML(raw_html)

        # in table there are 3 types of data:
        # 'Código': the code of a discipline that belongs to the
        #           current departament
        # 'Denominação': name of the discipline
        # 'Ementa': garbage (it was a icon with a link on
        #           the table, but those information where
        #           ignored when scrapping)

        # the table_data can be empty
        if (self.campus == 1):
            if table_data is not None:
                self.unprocessedDisciplines += [
                    {'Código': x['Código'],
                        'Denominação': x['Denominação']}
                    for x in table_data
                ]
                self.disciplines.append([
                    Discipline(x['Código'], x['Denominação'], self.code)
                    for x in table_data
                ])
