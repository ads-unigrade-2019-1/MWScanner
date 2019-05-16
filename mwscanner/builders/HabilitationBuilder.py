import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner import BASE_URL
from mwscanner.Mixins import UrlLoaderMixin
from mwscanner.Habilitation import Habilitation


class HabilitationBuilder(UrlLoaderMixin):

    def getDisciplineListURL(self, code):
        # This method take the url of the
        # disciplines from habilitation flow
        return BASE_URL + 'graduacao/fluxo.aspx?cod={}'.format(code)

    def buildFromHtml(self, code, name):
        # This method builds the list of disciplines that belongs
        # to this department. This list will be later used to
        # process the creation of the Discipline object.

        response = self.getFromUrl(self.getDisciplineListURL(code))

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

            disciplines = {}

            disciplines.update(
                {period: period_disciplines}
            )

        print("[Habilitation {}] Finished".format(name))
        return disciplines

    def buildHabilitation(self, code, name, degree):

        habilitation = Habilitation()
        habilitation.setName(name)
        habilitation.setCode(code)
        habilitation.setDegree(degree)
        habilitation.setDisciplines(self.buildFromHtml(code, name))

        return habilitation
