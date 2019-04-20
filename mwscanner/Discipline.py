import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner import BASE_URL
from mwscanner.Class import Class
from mwscanner.Mixins import TableReaderMixin, UrlLoaderMixin


class Discipline(TableReaderMixin, UrlLoaderMixin):
    # This class represents a Discipline present on
    # matriculaweb. it contains data about the discipline
    # and holds its classes and requirements

    def __init__(self, code, name, department):

        # name of the discipline
        self.name = name

        # identificator code for the discipline
        # (it's unique among disciplines)
        self.code = code

        # department to which this discipline belongs
        self.department = department

        # aumount of credits that this discipline
        # is worth
        # self.credits = discipline_credits

        # self.category = category

        # list with the Classes objects for this discipline
        self.classes = []

        # self relation with other Discipline objects that are
        # the requirements for the current discipline
        # Since there will be times when the required discipline will
        # no have been created, this will hold only the key (attribute code)
        # for the required disciplines
        self.requirements = []

        self.getClassesData()
        self.getRequirements()

    def getDisciplineOfferURL(self):
        # This method take the url of the
        # disciplines from the department code
        return BASE_URL + 'graduacao/oferta_dados.aspx?cod={}&dep={}'.format(
            self.code, self.department)

    def getDisciplineURL(self):
        # This method take the url of the
        # disciplines from the department code
        return BASE_URL + 'graduacao/disciplina.aspx?cod={}'.format(
            self.code)

    def getClassesData(self):

        response = self.getFromUrl(self.getDisciplineOfferURL())

        # Verify if the status cod is ok
        if response.status_code != 200:
            return

        found_classes = []

        # Make the parse for html
        # And read the table indentify in parse html
        raw_html = BeautifulSoup(response.content, 'lxml')

        classes_tables = raw_html.find_all(
            'table',
            {
                'id': 'datatable',
            }
        )

        if len(classes_tables) <= 0:
            return

        # The first element is always a table with discipline informations
        # it can be discarded before the next step
        del classes_tables[0]

        for class_table in classes_tables:
            c = Class.buildFromHtml(class_table, self)
            found_classes.append(c)

            print('[Discipline {}] Class {} finished'.format(self.name, c.name))

        print('[Discipline {}] finished'.format(self.name))

    def getRequirements(self):

        response = self.getFromUrl(self.getDisciplineURL())

        if response.status_code != 200:
            return

        raw_html = BeautifulSoup(response.content, 'lxml')

        requirements_table_row = raw_html.findAll(
            'th', text='Pré-requisitos')[0].parent

        found_requirements = []
        append_next = False


        for req in requirements_table_row.findAll('strong'):

            req = req.text.strip()

            if req == '' or req == 'E':
                continue

            if append_next:
                found_requirements[-1].append(req)
                append_next = False

            elif req == 'OU':
                if type(found_requirements[-1]) is not list:
                    found_requirements[-1] = [found_requirements[-1]]
                append_next = True

            else:
                found_requirements.append(
                    req
                )

        self.requirements = found_requirements
