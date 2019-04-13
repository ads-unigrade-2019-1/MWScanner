import sys

import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner import BASE_URL
from mwscanner.Mixins import TableReaderMixin, UrlLoaderMixin


class Discipline(TableReaderMixin, UrlLoaderMixin):
    # This class represents a Discipline present on
    # matriculaweb. it contains data about the discipline
    # and holds its classes and requirements

    def __init__(self, code, name, departament):

        # name of the discipline
        self.name = name

        # identificator code for the discipline
        # (it's unique among disciplines)
        self.code = code

        # departament to which this discipline belongs
        self.departament = departament

        # aumount of credits that this discipline
        # is worth
        # self.credits = discipline_credits

        # self.category = category

        # list with the Classes objects for this discipline
        self.classes = []

        # self relation with other Discipline objects that are
        # the requirements for the current discipline
        # Since there will be times when the required discipline will
        # no have been created, this will hold only the key (attribute code)
        # for the required disciplines
        self.requirements = []

        self.getClassesData()

    # METODO PARA CRIAR A URL
    def getDisciplineURL(self):
        # This method take the url of the
        # disciplines from the department code
        return BASE_URL + 'graduacao/oferta_dados.aspx?cod={}&dep={}'.format(
            self.code, self.departament)

    # METODO PARA PEGAR A URL E PEGAR OS DADOS E RETORNAR A DISCIPLINA
    def getClassesData(self):
        # Make response

        response = self.getFromUrl(self.getDisciplineURL())

        # Verify if the status cod is ok
        if response.status_code == 200:
            return

        found_classes = []

        # Make the parse for html
        # And read the table indentify in parse html
        raw_html = BeautifulSoup(response.content, 'html.parser')
        table_vacances = raw_html.find_all(
            'table', {'class': 'table tabela-vagas'})
        candidates_shift = raw_html.find_all('td', {'colspan': '2'})
        shift_turn = []
        filter_mettings = raw_html.find_all(
            'table', {
                'class': 'table table-striped table-bordered table-condensed'
            })

        meeting = []
        meetings = []

        for curretn in filter_mettings:
            meeting.append(curretn.text)

        number_classes = len(raw_html.find_all('td', {'class': 'turma'}))
        number_meetings = len(meeting)

        cont = 0

        if number_meetings > 0:

            for i in range(0, len(meeting), int(number_meetings / number_classes)):
                meetings.append(
                    meeting[i:i + int(number_meetings / number_classes)])

            for cand in candidates_shift:
                if cand.text == 'Diurno' or cand.text == 'Ambos' or cand.text == 'Noturno':
                    shift_turn.append(cand.text)

            str_html = str(raw_html)
            teachers = []

            designate_teacher = []

            if(str_html.find('<td>A Designar</table>')):
                for designate in re.finditer('A Designar</table>', str_html):
                    designate_teacher.append(designate.start())

            print(designate_teacher)

            for pos_teacher in re.finditer('<td><table><tr><td>', str_html):
                current_teacher = []
                position_current = pos_teacher.end()

                if designate_teacher != []:
                    for i in designate_teacher:
                        if i < position_current:
                            teachers.append(['A Designar'])
                            del i

                first_teacher = str_html[position_current:].partition(
                    "</td>")[0]
                next_verify = str_html[position_current:].partition(
                    "</td>")[2]
                current_teacher.append(first_teacher)

                if(next_verify[0:13] == '</tr><tr><td>'):
                    second_teacher = next_verify[13:]
                    second_teacher = second_teacher.partition("</td>")[0]
                    current_teacher.append(second_teacher)

                teachers.append(current_teacher)

            if designate_teacher != []:
                teachers.append(['A designar'])

            print(teachers)

            cont = 0
            for cla in raw_html.find_all('td', {'class': 'turma'}):
                found_classes.append(
                    {'class': cla.text, 'vacancies': table_vacances[cont].text, 'shift': shift_turn[cont], 'meetting': meetings[cont], 'teacher': teachers[cont]})
                cont += 1
            print(found_classes)

