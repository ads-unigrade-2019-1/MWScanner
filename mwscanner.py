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

        self.disciplines = []


class Campus():

    def __init__(self):
        self.all_campus_courses = {}
        self.courses = []
        self.all_campus_departments = {}
        self.departments = []

    def getCampusCoursesUrl(self, campus):
        return BASE_URL + 'graduacao/curso_rel.aspx?cod={}'.format(campus)

    def getCampusCourses(self, campus_code):

        response = get(self.getCampusCoursesUrl(campus_code))
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
                    #print(tableHeadList[0])
                    # Take off the first element in list and adding
                    # in final from the same list (queue)
                    tableHeadList.append(tableHeadList.pop(0))

                # Verify if the current course atribute is empty,
                # if not append in list of course
                if course_atributes != {}:
                    self.courses.append(
                        Course(campus_code, course_atributes['Código'], 
                        course_atributes['Denominação'], course_atributes['Turno'], 
                        course_atributes['Modalidade'])
                        )
                    list_courses.append(course_atributes)
        return list_courses

    def getAllCampusCourses(self):

        for campus, code in CAMPUS.items():
            self.all_campus_courses.update({
                campus: self.getCampusCourses(code)
            })
        return self.all_campus_courses


class Discipline():

    def __init__(self, code, name, departament, disciplineCredits, category):

        self.name = name
        self.code = code
        self.departament = departament
        self.credits = disciplineCredits
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


class Departament():
    pass

if __name__ == '__main__':
    campus = Campus()
    list_all_campus_courses = campus.getAllCampusCourses()
    print(list_all_campus_courses)