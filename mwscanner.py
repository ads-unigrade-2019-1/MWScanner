from mwscanner.Campus import Campus
from mwscanner.Discipline import Discipline
from dbConnection import Database


BASE_URL = 'https://matriculaweb.unb.br/'

if __name__ == '__main__':
    try:

        # creates a campus object, it will hold
        # information about the campi on the Matricula Web
        campus = Campus()

        # call methodes to scrap courses and departaments information
        # frow the Web
        # list_all_campus_courses = campus.getAllCampusCourses()
        list_all_campus_departments = campus.getAllCampusDepartments()

        # print all courses and habilitations founded
        # for course in campus.courses:
        #     print(
        #         "[CURSO] CÓDIGO: {} NOME: {} TURNO: {} MODALIDADE: {}".format(
        #             course.code, course.name, course.shift, course.modality)
        #     )
        # for habilitation in course.habilitations:
        #     print("[HABILITAÇÃO] CÓDIGO: {} NOME: {} GRAU: {}".format(
        #         habilitation.code, habilitation.name, habilitation.degree))

        #     habilitation.buildLinkList()

        #     print("[LISTA DE DISCIPLINAS POR PERÍODO] {}".format(
        #         habilitation.disciplines
        #     )
        #     )

        # prints departament information
        # and then build the list of disciplines that each departament have
        for departament in campus.departments:
            print("[DEPARTAMENTO] CÓDIGO: {} NOME: {} SIGLA: {}".format(
                departament.code, departament.name, departament.initials
            ))

            departament.buildLinkList()

            print("[LISTA DE DISCIPLINAS POR DEPARTAMENTO] {}".format(
                departament.unprocessedDisciplines
            ))

            for unprocessed_disclipline in departament.unprocessedDisciplines:

                departament.unprocessedDisciplines.remove(
                    unprocessed_disclipline
                )

                d = Discipline(
                    code=unprocessed_disclipline['Código'],
                    name=unprocessed_disclipline['Denominação'],
                    departament=departament
                )

                departament.disciplines.append(d)

    except KeyboardInterrupt:
        print('Interruption')
