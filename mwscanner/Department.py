import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner import BASE_URL
from mwscanner.Discipline import Discipline
from mwscanner.builders.DisciplinesBuilder import DisciplinesBuilder
from mwscanner.Mixins import TableReaderMixin, UrlLoaderMixin


class Department(TableReaderMixin, UrlLoaderMixin):

    def __init__(self):
        # department attributes
        self.__campus = 1
        self.__code = ""
        self.__name = ""
        self.__initials = ""

        self.__disciplines = []
        self.__unprocessedDisciplines = []

    def getCampus(self):
        return self.__campus

    def getCode(self):
        return self.__code

    def getName(self):
        return self.__name

    def getInitials(self):
        return self.__initials

    def getDisciplines(self):
        return self.__disciplines

    def setCampus(self, campus):
        if isinstance(campus, type(self.__campus)):
            self.__campus = campus

    def setName(self, name):
        if isinstance(name, type(self.__name)):
            self.__name = name

    def setInitials(self, initials):
        if isinstance(initials, type(self.__initials)):
            self.__initials = initials

    def setDisciplines(self, disciplines):
        if isinstance(disciplines, type(self.__disciplines)):
            self.__disciplines = disciplines

    def setCode(self, code):
        if isinstance(code, type(self.__code)):
            self.__code = code
