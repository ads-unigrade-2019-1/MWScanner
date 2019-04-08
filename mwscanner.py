from bs4 import BeautifulSoup
from requests import get
import json

BASE_URL = 'https://matriculaweb.unb.br/'
CAMPUS = {
    'darcy': 1,
    'planaltina': 2,
    'ceilandia': 3,
    'gama': 4
}


class Course:

    def __init__(self, code, name, campus):

        self.code = code
        self.name = name
        self.campus = campus
        self.disciplines = []

        return self


class CampusOperator:

    def getCampusUrl(campus):
        return BASE_URL + 'graduacao/curso_rel.aspx?cod={}'.format(campus[1])

    def getCampusCourses(campus_url):

        response = get(campus_url)
        list_courses = []

        if response.status_code == 200:

            # Make the parse for html
            raw_html = BeautifulSoup(response.content, 'html.parser')

            # Table head comment guide in table
            tableHeadList = []

            # Select all the th in html parser
            for table_head in raw_html.select('th'):
                tableHeadList.append(str(table_head.text))

            # Select all the rows in html
            for table_row in raw_html.select('tr'):
                course_atributes = {}

                # In all rows we take the data
                for table_data in table_row.select('td'):

                    if str(table_data.text) == '':
                        break

                    # Creating the dictionarie with the
                    # first element in table head list
                    # and data table text
                    course_atributes[tableHeadList[0]] = str(table_data.text)

                    # Take off the first element in list and adding
                    # in final from the same list (queue)
                    tableHeadList.append(tableHeadList.pop(0))

                # Verify if the current course atribute is empty,
                # if not append in list of course
                if course_atributes != {}:
                    list_courses.append(course_atributes)

        print(list_courses)

    def getAllCourses():

        courses = {}

        for campus in CAMPUS.items():

            courses.update({
                campus: getCampusCourses(getCampusUrl(campus))
            })

        return courses


class Discipline:

    def __init__(self, code, name, departament, disciplineCredits, category):

        self.name = name
        self.code = code
        self.departament = departament
        self.credits = disciplineCredits
        self.category = category

        self.classes = []
        self.requirements = []
        self.course = []

        return self


class Class:

    def __init__(self, name, vacancies, discipline):

        self.name = name
        self.vacancies = vacancies
        self.discipline = discipline

        self.rooms = []
        self.days = []
        self.hours = []

        return self


class Departament:
    pass