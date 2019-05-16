import requests
from bs4 import BeautifulSoup
from requests import get

from mwscanner import BASE_URL
from mwscanner.Discipline import Discipline
from mwscanner.Mixins import TableReaderMixin, UrlLoaderMixin
from mwscanner.Department import Department
from mwscanner.builders.DisciplinesBuilder import DisciplinesBuilder


class DepartmentBuilder(TableReaderMixin, UrlLoaderMixin):

    def getDisciplineListURL(self, code):
        # This method take the url of the
        # disciplines from the department code
        return BASE_URL + 'graduacao/oferta_dis.aspx?cod={}'.format(code)

    def buildFromHtml(self, code, name):
        # This method builds the list of disciplines that belongs
        # to this department. This list will be later used to
        # process the creation of the Discipline object.

        response = self.getFromUrl(self.getDisciplineListURL(code))

        if response.status_code != 200:
            return

        # Make the parse for html
        raw_html = BeautifulSoup(response.content, 'html.parser')
        table_data = self.readDatatableTableFromHTML(raw_html)

        # in table there are 3 types of data:
        # 'Código': the code of a discipline that belongs to the
        #           current department
        # 'Denominação': name of the discipline
        # 'Ementa': garbage (it was a icon with a link on
        #           the table, but those information where
        #           ignored when scrapping)

        # the table_data can be empty

        disciplines = []

        if table_data is not None:
            for x in table_data:
                disciplines.append(
                    DisciplinesBuilder().buildDiscipline(
                        x['Código'], x['Denominação'], code)
                )

        print("[Department {}] Finished".format(name))
        return disciplines

    def buildDepartment(self,  campus, code, name, initials):

        disciplines = self.buildFromHtml(code, name)

        department = Department()
        department.setCampus(campus)
        department.setCode(code)
        department.setDisciplines(disciplines)
        department.setIntials(initials)
        department.setName(name)

        return department
