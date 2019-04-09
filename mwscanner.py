from bs4 import BeautifulSoup
from requests import get
import json

BASE_URL = 'https://matriculaweb.unb.br/'
CAMPUS = {
    'Darcy Ribeiro': 1,
    'Planaltina': 2,
    'Ceilandia': 3,
    'Gama': 4
}


class Course():

    def __init__(self, campus, code, name, shift, modality):

        self.campus = campus
        self.code = code
        self.name = name
        self.shift = shift
        self.modality = modality

        self.discipline = []


class Department():

    def __init__(self, campus, code, name, initials):

        self.campus = campus
        self.code = code
        self.name = name
        self.initials = initials

        self.disciplines_offers = []


class Campus():

    def __init__(self):
        self.all_campus_courses = {}
        self.courses = []
        self.all_campus_departments = {}
        self.departments = []

    def getCampusCoursesUrl(self, campus):
        return BASE_URL + 'graduacao/curso_rel.aspx?cod={}'.format(campus)

    def getCampusDepartmentsUrl(self, campus):
        return BASE_URL + 'graduacao/oferta_dep.aspx?cod={}'.format(campus)

    def getCampusCourses(self, campus_code):

        response = get(self.getCampusCoursesUrl(campus_code))
        list_courses = []

        if response.status_code == 200:

            # Make the parse for html
            raw_html = BeautifulSoup(response.content, 'html.parser')

            # Table head comment guide in table
            table_head_list = []

            # Select all the th in html parser
            for table_head in raw_html.select('th'):
                table_head_list.append(str(table_head.text))

            # Select all the rows in html
            for table_row in raw_html.select('tr'):
                course_attributes = {}

                # In all rows we take the data
                for table_data in table_row.select('td'):

                    if str(table_data.text) == '':
                        break

                    # Creating the dictionarie with the
                    # first element in table head list
                    # and data table text
                    course_attributes[table_head_list[0]] = str(
                        table_data.text)
                    # Take off the first element in list and adding
                    # in final from the same list (queue)
                    table_head_list.append(table_head_list.pop(0))

                # Verify if the current course attribute is empty,
                # if not append in list of course
                if course_attributes != {}:
                    self.courses.append(
                        Course(
                            campus_code,
                            course_attributes['Código'],
                            course_attributes['Denominação'],
                            course_attributes['Turno'],
                            course_attributes['Modalidade'])
                    )
                    list_courses.append(course_attributes)
        return list_courses

    def getCampusDepartments(self, campus_code):

        response = get(self.getCampusDepartmentsUrl(campus_code))
        list_departments = []

        if response.status_code == 200:

            # Make the parse for html
            raw_html = BeautifulSoup(response.content, 'html.parser')

            # Table head comment guide in table
            table_head_list = []

            # Select all the th in html parser
            for table_head in raw_html.select('th'):
                table_head_list.append(str(table_head.text))

            # Select all the rows in html
            for table_row in raw_html.select('tr'):
                department_attributes = {}

                # In all rows we take the data
                for table_data in table_row.select('td'):

                    if str(table_data.text) == '':
                        break

                    # Creating the dictionary with the
                    # first element in table head list
                    # and data table text
                    department_attributes[table_head_list[0]] = str(
                        table_data.text)
                    # Take off the first element in list and adding
                    # in final from the same list (queue)
                    table_head_list.append(table_head_list.pop(0))

                # Verify if the current department attribute is empty,
                # if not append in list of department
                if department_attributes != {}:
                    self.departments.append(
                        Department(
                            campus_code,
                            department_attributes['Código'],
                            department_attributes['Denominação'],
                            department_attributes['Sigla']
                        )
                    )
                    list_departments.append(department_attributes)
        return list_departments

    def getAllCampusCourses(self):

        for campus, code in CAMPUS.items():
            self.all_campus_courses.update({
                campus: self.getCampusCourses(code)
            })
        return self.all_campus_courses

    def getAllCampusDepartments(self):

        for campus, code in CAMPUS.items():
            self.all_campus_departments.update({
                campus: self.getCampusDepartments(code)
            })
        return self.all_campus_departments


class Discipline():

    def __init__(self, code, name, departament, discipline_credits, category):

        self.name = name
        self.code = code
        self.departament = departament
        self.credits = discipline_credits
        self.category = category

        self.classes = []
        self.requirements = []
        self.course = []


class Class():

    def __init__(self, name, vacancies, discipline):

        self.name = name
        self.vacancies = vacancies
        self.discipline = discipline

        self.rooms = []
        self.days = []
        self.hours = []


if __name__ == '__main__':
    campus = Campus()
    list_all_campus_courses = campus.getAllCampusCourses()
    print(list_all_campus_courses)
    list_all_campus_departments = campus.getAllCampusDepartments()
    print(list_all_campus_departments)
