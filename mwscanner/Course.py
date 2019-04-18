import re
import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner.Habilitation import Habilitation
from mwscanner.Mixins import UrlLoaderMixin


from mwscanner import BASE_URL


class Course(UrlLoaderMixin):
    # This class represents a course registered on the Matricula
    # Web. It has the information about this course.

    def __init__(self, campus, code, name, shift, modality):

        # Campus where this course belongs
        self.campus = campus

        # Code for the course (unique)
        self.code = code

        # Course name
        self.name = name

        # Course shift (Ex: 'Diurno', 'Noturno')
        self.shift = shift

        # Type of degree this course provides
        self.modality = modality
        # Course habilitations, a course curriculum can change
        # based on its habilitations
        self.habilitations = []

        # Method to initialize habilitations with course habilitations
        self.getHabilitations(self.code)

    def getHabilitations(self, code):

        response = self.getFromUrl(
            BASE_URL + 'graduacao/curso_dados.aspx?cod={}'.format(
                self.code)
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

        # append habilitations data in list
        for i in range(len(codes)):
            self.habilitations.append(
                Habilitation(
                    codes[i], names[i], degrees[i]
                )
            )
            print("[COURSE {}] Got Habilitation {}".format(self.name, names[i]))
