from bs4 import BeautifulSoup
from requests import get
import json

BASE_URL = 'https://matriculaweb.unb.br/'

# Campus index for guide in url search
CAMPUS = {
    'Darcy Ribeiro': 1,
    'Planaltina': 2,
    'Ceilandia': 3,
    'Gama': 4
}


class TableReader:
# Abstract class that provides methods for the 
# reading of tables on pages of Matricula Web 
# website. This is inherithed in a scheme that allow
# multiple inheritance, thus acting, in a way, similarly
# to Java Interfaces.

    @staticmethod
    def readSimpleTableFromHTML(raw_html):
    # This method is capable of reading tables on
    # pages that use the common layout on Matricula
    # Web. It recieves the raw_html element (returned from
    # BeautifulSoup) and process it.
    # It returns a list in which each element is a dictionarie
    # that has the following structure:
    # {
    #   'table_head_name': 'table_row_attribute',
    #   ...
    # }

        # Table head comment guide in table
        table_head_list = []
        extracted_data = []

        # Select all the th in html parser
        for table_head in raw_html.select('th'):
            table_head_list.append(str(table_head.text))

        # Select all the rows in html
        for table_row in raw_html.select('tr'):
            attributes = {}

            # In all rows we take the data
            for table_data in table_row.select('td'):

                if str(table_data.text) == '':
                    break

                # Creating the dictionarie with the
                # first element in table head list
                # and data table text
                attributes[table_head_list[0]] = str(
                    table_data.text
                )

                # Take off the first element in list and adding
                # in final from the same list (queue)
                table_head_list.append(table_head_list.pop(0))

            # Verify if the current course attribute is empty,
            # if not append in list of course
            if attributes != {}:
                extracted_data.append(attributes)

        return extracted_data

    @staticmethod
    def readDatatableTableFromHTML(raw_html):
    # This method is capable of reading tables on
    # pages that use the datatable layout on Matricula
    # Web. It recieves the raw_html element (returned from
    # BeautifulSoup) and process it.
    # It returns a list in which each element is a dictionarie
    # that has the following structure:
    # {
    #   'table_head_name': 'table_row_attribute',
    #   ...
    # }

        # Table head comment guide in table
        table_head_list = []
        extracted_data = []

        datatable_div = raw_html.select('#datatable')

        if len(datatable_div) == 0:
            return None

        # Select all the rows in html
        for table_row in datatable_div[0].select('tr'):

            if len(table_head_list) == 0:
                for th in table_row.select('th'):
                    table_head_list.append(str(th.text))
                continue

            attributes = {}

            # In all rows we take the data
            for table_data in table_row.select('td'):

                if str(table_data.text) == '':
                    break

                # Creating the dictionarie with the
                # first element in table head list
                # and data table text
                attributes[table_head_list[0]] = str(
                    table_data.text
                )

                # Take off the first element in list and adding
                # in final from the same list (queue)
                table_head_list.append(table_head_list.pop(0))

            # Verify if the current course attribute is empty,
            # if not append in list of course
            if attributes != {}:
                extracted_data.append(attributes)

        return extracted_data


class Course():
# This class represents a course registered on the Matricula
# Web. It has the information about this course.

    def __init__(self, campus, code, name, shift, modality):

        # Campus where this course belongs
        self.campus = campus

        # Code for the course (unique)
        self.code = code

        # Course name
        self.name = name

        # Course shift (Ex: 'Matutino', 'Integral')
        self.shift = shift

        # Type of degree this course provides
        self.modality = modality

        # This represents the disciplines associated with this
        # course. The data here wiil be on the following format:
        # disciplines == [
        #   'PERIOD_NUMBER': [list with the code for the discipline of this period]
        #   ...
        # ]
        self.disciplines = []


class Department(TableReader):

    def __init__(self, campus, code, name, initials):

        self.campus = campus
        self.code = code
        self.name = name
        self.initials = initials

        self.disciplines = []
        self.unprocessedDisciplines = []

    def getDisciplineListURL(self):
        return BASE_URL + 'graduacao/oferta_dis.aspx?cod={}'.format(self.code)

    def buildLinkList(self):
    # This method builds the list of disciplines that belongs
    # to this departament. This list will be later used to
    # process the creation of the Discipline object.

        response = get(self.getDisciplineListURL())

        if response.status_code == 200:

            # Make the parse for html
            raw_html = BeautifulSoup(response.content, 'html.parser')
            table_data = self.readDatatableTableFromHTML(raw_html)

            # in table there are 3 types of data:
            # 'Código': the code of a discipline that belongs to the
            #           current departament
            # 'Denominação': name of the discipline
            # 'Ementa': garbage (it was a icon with a link on
            #           the table, but those information where
            #           ignored when scrapping)

            # the table_data can be empty
            if table_data is not None:
              self.unprocessedDisciplines += [
                {'Código': x['Código'], 'Denominação': x['Denominação']}
                for x in table_data
              ]


class Campus(TableReader):
# This class represent all the 4 campus prensent in UnB

		# Define the atributes basics from all campus 
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
        response = get(self.getCampusCoursesUrl(campus_code))
        list_courses = []

				# if the status code is "ok"
        if response.status_code == 200:

            # Make the parse for html using beautifulsoap
						# Read the data from table using the parser
            raw_html = BeautifulSoup(response.content, 'html.parser')
            table_data = self.readSimpleTableFromHTML(raw_html)

						# According the row in each table we take the especific 
						# colum in table and create a instance from course
						# and seve in list courses from campus
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
        response = get(self.getCampusDepartmentsUrl(campus_code))
        list_departments = []

				# Verify if the status cod is ok
        if response.status_code == 200:

            # Make the parse for html
						# And read the table indentify in parse html
            raw_html = BeautifulSoup(response.content, 'html.parser')
            table_data = self.readSimpleTableFromHTML(raw_html)

						# For all row in table, an object Departament
						# is create and added in list of departaments
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
		# the list of all departaments and return an dictionary for
		# that specific campus 
    def getAllCampusDepartments(self):

        for campus, code in CAMPUS.items():
            self.all_campus_departments.update({
                campus: self.getCampusDepartments(code)
            })
        return self.all_campus_departments


class Discipline():
# This class represents a Discipline present on
# matriculaweb. it contains data about the discipline
# and holds its classes and requirements

    def __init__(self, code, name, departament, discipline_credits, category):

        # name of the discipline
        self.name = name

        # identificator code for the discipline 
        # (it's unique among disciplines)
        self.code = code
        
        # departament to which this discipline belongs
        self.departament = departament

        # aumount of credits that this discipline
        # is worth
        self.credits = discipline_credits


        self.category = category

        # list with the Classes objects for this discipline
        self.classes = []

        # self relation with other Discipline objects that are
        # the requirements for the current discipline
        # Since there will be times when the required discipline will
        # no have been created, this will hold only the key (attribute code)
        # for the required disciplines
        self.requirements = []

        # courses that have this discipline on its curriculum
        self.courses = []


class Class():
# This class represents a discipline class on Matricula
# Web. It contains data about the meetings and a
# connection to the discipline.


    def __init__(self, name, vacancies, discipline):

        # name of class, example: "Turma A"
        # this is unique inside a discipline
        self.name = name

        # number of available vacancies in this class
        self.vacancies = vacancies

        # discipline in which this class belongs
        self.discipline = discipline

        # a meeting should have the structure:
        # {
        #   room: str
        #   day: str
        #   hour: str
        # }
        self.meetings = []

    def appendMeeting(self, room, day, hour):
    # adds a meeting to this class list of meetings
    # all parameters are strings
    # room: room where the meeting will occour
    # day: weekday of the meeting
    # hour: time of the meeting


        self.meetings.append({
            'room': room,
            'day': day,
            'hour': hour
        })


if __name__ == '__main__':

    # creates a campus object, it will hold
    # information about the campi on the Matricula Web
    campus = Campus()

    # call methodes to scrap courses and departaments information
    # frow the Web
    list_all_campus_courses = campus.getAllCampusCourses()
    list_all_campus_departments = campus.getAllCampusDepartments()
    
    # pprint all courses found
    for course in campus.courses:
      print("COURSE - COD: {} NOME: {}".format(course.code, course.name))

    # prints departament information
    # and then build the list of disciplines that each departament have
    for departament in campus.departments:
        print("DEP - COD: {} NOME: {}".format(departament.code, departament.name))
        departament.buildLinkList()
