import re
import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner.Course import Course
from mwscanner.Mixins import UrlLoaderMixin
from mwscanner.Habilitation import Habilitation
from mwscanner.builders.HabilitationBuilder import HabilitationBuilder
from mwscanner import BASE_URL

class CourseBuilder(UrlLoaderMixin):

    def __init__(self):
        pass

    def getHabilitations(self, code):

        response = self.getFromUrl(
            BASE_URL + 'graduacao/curso_dados.aspx?cod={}'.format(
                code)
        )

        if response.status_code != 200:
            return

        raw_html = BeautifulSoup(response.content, 'html.parser')

        # lists to take each habilitation data
        codes = []
        names = []
        degrees = []

        # take codes and names from page
        for h4 in raw_html.select('h4'):
            # Separate the h4 in two parts
            # code and name using regex
            habilitation_code = (int(
                (re.search(r"\d+", h4.text)).group()))

            habilitation_name = (
                re.search(r"\D+", h4.text)
            ).group().rstrip()

            codes.append(habilitation_code)
            names.append(habilitation_name)

        # take degrees from page
        for tr in raw_html.select('tr'):
            if tr.th.text == 'Grau':
                habilitation_degree = tr.td.text
                degrees.append(habilitation_degree)

        habilitations = []

        # append habilitations data in list
        for i in range(len(codes)):
            habilitations.append(
                HabilitationBuilder().buildHabilitation(
                    codes[i], names[i], degrees[i]
                )
            )
            print("[COURSE {}] Got Habilitation {}".format(
            '', names[i]))
    