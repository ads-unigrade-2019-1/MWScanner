import re
import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner.Habilitation import Habilitation
from mwscanner.builders.HabilitationBuilder import HabilitationBuilder
from mwscanner.Mixins import UrlLoaderMixin


from mwscanner import BASE_URL


class Course(UrlLoaderMixin):
    # This class represents a course registered on the Matricula
    # Web. It has the information about this course.

    def __init__(self):

        # Campus where this course belongs
        self.__campus = 1

        # Code for the course (unique)
        self.__code = ""

        # Course name
        self.__name = ""

        # Course shift (Ex: 'Diurno', 'Noturno')
        self.__shift = ""

        # Type of degree this course provides
        self.__modality = ""
        # Course habilitations, a course curriculum can change
        # based on its habilitations
        self.__habilitations = []

        # Method to initialize habilitations with course habilitations

    def getCampus (self):
        return self.__campus
    
    def getCode (self):
        return self.__code
    
    def getName (self):
        return self.__name

    def getShift (self):
        return self.__shift

    def getModality (self):
        return self.__modality

    def getHabilitations (self):
        return self.__habilitations

    def setCampus (self, campus):
        if isinstance(campus, type(self.__campus)):
            self.__campus = campus 

    def setCode (self, code):
        if isinstance(code, type(self.__code)):
            self.__code = code 

    def setName (self, name):
        if isinstance(name, type(self.__name)):
            self.__name = name

    def setShift (self, shift):
        if isinstance(shift, type(self.__shift)):
            self.__shift = shift 

    def setModality (self, modality):
        if isinstance(modality, type(self.__modality)):
            self.__modality = modality 

    def setHabilitations (self, Habilitation):
        if isinstance(Habilitation, type(self.__habilitations)):
            self.__habilitations = Habilitation 
        

    
