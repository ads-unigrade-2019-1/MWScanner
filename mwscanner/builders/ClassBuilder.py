from mwscanner.Class import Class


class ClassBuilder:

    def __init__(self):
        pass

    def extractClassName(self, raw_html):
        # returns the text present on the table
        # access respecting the HTML order
        td_list = raw_html.find_all('td', 'turma')

        return td_list[0].text

    def extractVacancies(self, raw_html):
        # This method extracted and return the vacancies from current class
        vacancies_table = raw_html.findAll('table')[0]

        vacancies_rows = vacancies_table.find_all('tr')
        vacancies = int(vacancies_rows[2].find_all('td')[2].text)

        # chose the row and get the freshaman vacancies and the total vacancies
        # and sum it
        if len(vacancies_rows) > 3:

            freshman_vacancies = int(vacancies_rows[5].find_all('td')[2].text)
            vacancies += freshman_vacancies

        return vacancies

    def extractShift(self, raw_html):
        # extract class shift
        return raw_html.text

    def extractMeetings(self, raw_html):
        # extract the meetings from the page
        meetings_tables = raw_html.findAll('table')
        meetings = []

        for table in meetings_tables:
            data = table.findAll('td')

            day = data[0].text
            init_hour = data[1].text
            final_hour = data[2].text
            room = data[4].text

            # search for all table data in current table
            # and get the day, current hour from class, room and return it
            meetings.append({
                'day': day,
                'init_hour': init_hour,
                'final_hour': final_hour,
                'room': room
            })

        return meetings

    def extractTeachers(self, raw_html):
        # Method to get all the teacher from one class

        return [x.text for x in raw_html.select('tr')]

    def buildFromHtml(self, raw_html, discipline, department):
        # Method which get all the atributes from methods above and create a
        # unique object Class

        # Get the extracted atributes from methods above
        class_data = {}
        extraction_order = [
            (self.extractClassName, 'name'),
            (self.extractVacancies, 'vacancies'),
            (self.extractShift, 'shift'),
            (self.extractMeetings, 'meetings'),
            (self.extractTeachers, 'teachers')
        ]

        # Search for all table rows and get the first one
        inner_table = raw_html.tbody.findAll('tr')[0]

        for td in inner_table:

            # if all steps where made
            if len(extraction_order) == 0:
                break

            # Pop one by one and add in class dict
            step = extraction_order.pop(0)

            class_data.update({
                step[1]: step[0](td)
            })

        class_data.update({'discipline': discipline})
        class_data.update({'department': department})

        # returned the object class created
        class_set = Class()
        class_set.setName(class_data['name'])
        class_set.setVacancies(class_data['vacancies'])
        class_set.setDiscipline(class_data['discipline'])
        class_set.setMettings(class_data['meetings'])
        class_set.setShift(class_data['shift'])
        class_set.setTeachers(class_data['teachers'])
        class_set.setDepartment(class_data['department'])

        return class_set
