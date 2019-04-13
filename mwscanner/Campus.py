import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner.Course import Course
from mwscanner.Departament import Department
from mwscanner.Mixins import TableReaderMixin, UrlLoaderMixin
from mwscanner import BASE_URL

# Campus index for guide in url search
CAMPUS = {
    'Darcy Ribeiro': 1,
    'Planaltina': 2,
    'Ceilandia': 3,
    'Gama': 4
}


class Campus(TableReaderMixin, UrlLoaderMixin):
    # This class represent all the 4 campus prensent in UnB

    # Define the attributes basics from all campus
    def __init__(self):

        self.all_campus_courses = {}
        self.courses = []

        self.all_campus_departments = {}
        self.departments = []

    # This method return all the courses
    # present in campus pass by parameter
    def getCampusCoursesUrl(self, campus):
        return BASE_URL + 'graduacao/curso_rel.aspx?cod={}'.format(campus)

    # This method return all the Departaments present
    # in campus passed by parameter
    def getCampusDepartmentsUrl(self, campus):
        return BASE_URL + 'graduacao/oferta_dep.aspx?cod={}'.format(campus)

    # This method return the list of courses from campus
    def getCampusCourses(self, campus_code):

        # Make the response according the campus URL and
        # initiate the list of courses

        response = self.getFromUrl(self.getCampusCoursesUrl(campus_code))

        # only proceed if the status code is "ok"
        if response.status_code != 200:
            return None

        list_courses = []

        # Make the parse for html using beautifulsoap
        # Read the data from table using the parser
        raw_html = BeautifulSoup(response.content, 'html.parser')
        table_data = self.readSimpleTableFromHTML(raw_html)

        # According the row in each table we take the specific
        # column in table and create a instance from course
        # and save in list courses from campus
        for data in table_data:
            self.courses.append(
                Course(
                    campus=campus_code,
                    code=data['Código'],
                    name=data['Denominação'],
                    shift=data['Turno'],
                    modality=data['Modalidade']
                )
            )
            list_courses.append(data)

        return list_courses

    # This method using the function above to create
    # the list of all courses and create an dict for
    # that specific campus
    def getAllCampusCourses(self):

        for campus, code in CAMPUS.items():
            self.all_campus_courses.update({
                campus: self.getCampusCourses(code)
            })
        return self.all_campus_courses

    # This method using the index campus and access
    # all the departament for that specifc campus
    def getCampusDepartments(self, campus_code):

        # Make response and initialize the list of departaments

        response = self.getFromUrl(self.getCampusDepartmentsUrl(campus_code))

        # Verify if the status code is ok
        if response.status_code == 200:
            return None

        list_departments = []

        # Make the parse for html
        # And read the table identify in parse html
        raw_html = BeautifulSoup(response.content, 'html.parser')
        table_data = self.readSimpleTableFromHTML(raw_html)

        # For all row in table, an object Departament
        # is create and added in list of departments
        for data in table_data:
            self.departments.append(
                Department(
                    campus=campus_code,
                    code=data['Código'],
                    name=data['Denominação'],
                    initials=data['Sigla']
                )
            )
            list_departments.append(data)

        return list_departments

    # This method using the function above to create
    # the list of all departments and return an dictionary for
    # that specific campus
    def getAllCampusDepartments(self):

        for campus, code in CAMPUS.items():
            self.all_campus_departments.update({
                campus: self.getCampusDepartments(code)
            })
        return self.all_campus_departments
