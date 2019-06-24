import re

from bs4 import BeautifulSoup

from mwscanner.Course import Course
from mwscanner.Mixins import UrlLoaderMixin
from mwscanner.builders.HabilitationBuilder import HabilitationBuilder
from mwscanner import BASE_URL


class CourseBuilder(UrlLoaderMixin):

    def __init__(self):
        pass

    def getHabilitations(self, code, name):

        response = self.getFromUrl(
            BASE_URL + 'graduacao/curso_dados.aspx?cod={}'.format(
                code)
        )

        if response.status_code != 200:
            return

        raw_html = BeautifulSoup(response.content, 'html.parser')

        # lists to take each habilitation data
        codes = []
        names = []
        degrees = []
        habilitations = []

        # take codes and names from page
        for h4 in raw_html.select('h4'):
            # Separate the h4 in two parts
            # code and name using regex
            habilitation_code = (int(
                (re.search(r"\d+", h4.text)).group()))

            habilitation_name = (
                re.search(r"\D+", h4.text)
            ).group().rstrip()

            codes.append(habilitation_code)
            names.append(habilitation_name)

        # take degrees from page
        for tr in raw_html.select('tr'):
            if tr.th.text == 'Grau':
                habilitation_degree = tr.td.text
                degrees.append(habilitation_degree)

        # append habilitations data in list
        for i in range(len(codes)):
            habilitations.append(
                HabilitationBuilder().buildHabilitation(
                    str(codes[i]), names[i], degrees[i]
                )
            )
            print("[COURSE {}] Got Habilitation {}".format(
                name, names[i]))

        return habilitations

    def builderCourse(self, campus, code, name, shift, modality):

        course = Course()
        course.setCampus(campus)
        course.setCode(code)
        course.setHabilitations(self.getHabilitations(code, name))
        course.setModality(modality)
        course.setName(name)
        course.setShift(shift)

        return course
