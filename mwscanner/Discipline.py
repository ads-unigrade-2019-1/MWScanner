import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner import BASE_URL
from mwscanner.Mixins import TableReaderMixin, UrlLoaderMixin
from mwscanner.builders.ClassBuilder import ClassBuilder


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
        self.credits = None

        # list with the Classes objects for this discipline
        self.classes = []

        # self relation with other Discipline objects that are
        # the requirements for the current discipline
        # Since there will be times when the required discipline will
        # no have been created, this will hold only the key (attribute code)
        # for the required disciplines
        self.requirements = []

        self.getCredits()
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

    def getCredits(self):
        # This method get the credits from current disciplines

        response = self.getFromUrl(self.getDisciplineOfferURL())

        if response.status_code != 200:
            return

        # Get the pattern in html evidenced by xxx-xxx-xxx-xxx
        raw_html = BeautifulSoup(response.content, 'lxml')
        credits_th = raw_html.findAll(
            'small', text='(Teor-Prat-Ext-Est)')

        if len(credits_th) == 0:
            return

        # Get the td respected pattern from text filtered
        credits_tr = credits_th[0].parent.parent
        discipline_credits_td = credits_tr.findAll('td')
        discipline_credits = discipline_credits_td[0].text

        self.credits = discipline_credits

    def getClassesData(self):

        response = self.getFromUrl(self.getDisciplineOfferURL())

        # Verify if the status cod is ok
        if response.status_code != 200:
            return

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

        classes_names = []

        for class_table in classes_tables:
            c = ClassBuilder().buildFromHtml(raw_html=class_table, discipline=self, department=self.department)
            self.classes.append(c)
            classes_names.append(c.getName())

        print('[Discipline {}] finished with classes {}'.format(
            self.name, classes_names))

    def getRequirements(self):
        # This method get all the requirements from the current discipline

        response = self.getFromUrl(self.getDisciplineURL())

        if response.status_code != 200:
            return

        raw_html = BeautifulSoup(response.content, 'lxml')

        # Search in html all the table heads with text "Pré requisito"
        requirements_table_row = raw_html.findAll(
            'th', text='Pré-requisitos')[0].parent

        found_requirements = []
        append_next = False

        # Use the strong elements to guide the requirement to be
        # U or E
        for req in requirements_table_row.findAll('strong'):

            req = req.text.strip()

            if req == '' or req == 'OU':
                continue

            # If append next is true we get and append the current
            # requirement to list of requeriment
            if append_next:
                found_requirements[-1].append(req)
                append_next = False

            # If it is E, only append the current to the last element
            # from list of found requirements
            elif req == 'E':
                if type(found_requirements[-1]) is not list:
                    found_requirements[-1] = [found_requirements[-1]]
                append_next = True
            # If there is no element, or is not OU or E, only
            # add it in list
            else:
                found_requirements.append(
                    req
                )

        self.requirements = found_requirements
