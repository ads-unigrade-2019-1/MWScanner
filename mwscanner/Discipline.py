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

    def __init__(self,):

        # name of the discipline
        self.__name = ""

        # identificator code for the discipline
        # (it's unique among disciplines)
        self.__code = ""

        # department to which this discipline belongs
        self.__department = ""

        # aumount of credits that this discipline
        # is worth
        self.__credits = None

        # list with the Classes objects for this discipline
        self.__classes = []

        # self relation with other Discipline objects that are
        # the requirements for the current discipline
        # Since there will be times when the required discipline will
        # no have been created, this will hold only the key (attribute code)
        # for the required disciplines
        self.__requirements = []

    def getName(self):
        return self.__name

    def setName(self, name):
        if isinstance(name, type(self.__name)):
            self.__name = name

    def getCode(self):
        return self.__code

    def setCode(self, code):
        if isinstance(code, type(self.__code)):
            self.__code = code

    def getDepartment(self):
        return self.__department

    def setDepartment(self, department):
        if isinstance(department, type(self.__department)):
            self.__department = department

    def getCredits(self):
        return self.__credits

    def setCredits(self, credit):
            self.__credits = credit

    def getClasses(self):
        return self.__classes

    def setClasses(self, classes):
        if isinstance(classes, list):
            self.__classes = classes

    def getRequirements(self):
        return self.__requirements

    def setRequirements(self, requirements):
        if isinstance(requirements, list):
            self.__requirements = requirements
