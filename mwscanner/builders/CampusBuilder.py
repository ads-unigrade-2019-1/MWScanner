import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner.builders.CoursesBuilder import CourseBuilder
from mwscanner.builders.DepartmentBuilder import DepartmentBuilder
from mwscanner.Department import Department
from mwscanner.Mixins import TableReaderMixin, UrlLoaderMixin
from mwscanner.Campus import Campus
from mwscanner import BASE_URL
from multiprocessing.dummy import Pool as ThreadPool

# Campus index for guide in url search
CAMPUS = {
    'Darcy Ribeiro': 1,
    'Planaltina': 2,
    'Ceilandia': 3,
    'Gama': 4
}


class CampusBuilder(TableReaderMixin, UrlLoaderMixin):

    def __init__(self):
        self.departments = []
        self.courses = []

    # This method return all the courses
    # present in campus pass by parameter
    def getCampusCoursesUrl(self, campus):
        return BASE_URL + 'graduacao/curso_rel.aspx?cod={}'.format(campus)

    # This method return all the departments present
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

        # Make the parse for html using beautifulsoap
        # Read the data from table using the parser
        raw_html = BeautifulSoup(response.content, 'html.parser')
        table_data = self.readSimpleTableFromHTML(raw_html)

        # According the row in each table we take the specific
        # column in table and create a instance from course
        # and save in list courses from campus

        def createCourses(data):

            course = CourseBuilder().builderCourse(
                campus=campus_code,
                code=data['Código'],
                name=data['Denominação'],
                shift=data['Turno'],
                modality=data['Modalidade']
            )

            self.courses.append(
                course
            )

            return course

        pool = ThreadPool(16)
        c = pool.map(createCourses, table_data)
        pool.close()
        pool.join()

        return self.courses

    # This method using the function above to create
    # the list of all courses and create an dict for
    # that specific campus
    def getAllCampusCourses(self):

        all_campus_courses = {}

        for campus, code in CAMPUS.items():
            all_campus_courses.update({
                campus: self.getCampusCourses(code)
            })
        return all_campus_courses

    # This method using the index campus and access
    # all the department for that specifc campus
    def getDepartments(self, campus_code):

        # Make response and initialize the list of departments

        response = self.getFromUrl(self.getCampusDepartmentsUrl(campus_code))

        # Verify if the status code is ok
        if response.status_code != 200:
            return None

        # Make the parse for html
        # And read the table identify in parse html
        raw_html = BeautifulSoup(response.content, 'html.parser')
        table_data = self.readSimpleTableFromHTML(raw_html)

        # For all row in table, an object department
        # is create and added in list of departments

        def createDepartments(data):

            depart = DepartmentBuilder().buildDepartment(
                campus=campus_code,
                code=data['Código'],
                name=data['Denominação'],
                initials=data['Sigla']
            )

            self.departments.append(
                depart
            )

            print("[CAMPUS] Found department {}".format(depart.getName()))

            return depart

        pool = ThreadPool(16)
        c = pool.map(createDepartments, table_data)
        pool.close()
        pool.join()

        return self.departments

    # This method using the function above to create
    # the list of all departments and return an dictionary for
    # that specific campus
    def getCampusDepartments(self):

        all_campus_departments = {}

        for campus, code in CAMPUS.items():
            all_campus_departments.update({
                campus: self.getDepartments(code)
            })
        return all_campus_departments

    def buildCampus(self):

        campus = Campus()

        campus.setAllCampusDepartments(self.getCampusDepartments())
        campus.setDepartments(self.departments)
        campus.setAllCampusCourses(self.getAllCampusCourses())
        campus.setCourses(self.courses)

        return campus
