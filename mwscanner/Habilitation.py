import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner import BASE_URL
from mwscanner.Mixins import UrlLoaderMixin


class Habilitation(UrlLoaderMixin):
    def __init__(self, code, name, degree):
        self.code = code
        self.name = name
        self.degree = degree

        # This represents the disciplines associated with this
        # course. The data here wiil be on the following format:
        # disciplines = {
        #   'PERIOD_NUMBER': [list with the code for the
        #                     discipline of this period]
        #   ...
        # }
        self.disciplines = {}

    def getDisciplineListURL(self):
        # This method take the url of the
        # disciplines from habilitation flow
        return BASE_URL + 'graduacao/fluxo.aspx?cod={}'.format(self.code)

    def buildLinkList(self):
        # This method builds the list of disciplines that belongs
        # to this departament. This list will be later used to
        # process the creation of the Discipline object.

        response = self.getFromUrl(self.getDisciplineListURL())

        if response.status_code != 200:
            return

        raw_html = BeautifulSoup(response.content, 'html.parser')
        # scrolls through tables with datatable id
        periods_tables = raw_html.find_all(id="datatable")

        for period_table in periods_tables:
            # picks up the period information that is in the tablehead
            period_infos = period_table.find_all('th')
            period = period_infos[1].text

            # take the information of the disciplines
            # of the period that are in the td
            disciplines_infos = period_table.find_all('td')

            period_disciplines = []
            for i in range(0, len(disciplines_infos), 6):

                discipline_code = int(disciplines_infos[3 + i].text)
                discipline_name = disciplines_infos[4 + i].text.rstrip()

                period_disciplines.append(
                    {'Código': discipline_code,
                        'Nome': discipline_name}
                )

            self.disciplines.update(
                {period: period_disciplines}
            )
