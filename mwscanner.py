from multiprocessing.pool import ThreadPool

from mwscanner.Campus import Campus
from mwscanner.Discipline import Discipline


BASE_URL = 'https://matriculaweb.unb.br/'


def proccessHabilitations(campus: Campus):

    all_habilitations = []

    t_pool = ThreadPool(processes=8)
    async_tasks = []

    courses_len = len(campus.courses)

    for index, course in enumerate(campus.courses):

        for habilitation in course.habilitations:

            async_tasks.append(
                (t_pool.apply_async(habilitation.buildFromHtml), index + 1)
            )
            all_habilitations.append(habilitation)

    for x in async_tasks:

        x[0].wait()

        print(
            "[HABILITATIONS] Course Progress: {} of {} ({}%)".format(
                x[1],
                courses_len,
                round(x[1]*100/courses_len, 2)
            ))

    return all_habilitations


def proccessDisciplines(campus: Campus):

    all_disciplines = []

    t_pool = ThreadPool(processes=16)
    async_tasks = []

    departments_len = len(campus.departments)

    def departament_scanner(departament):

        departament.buildFromHtml()

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
            all_disciplines.append(d)

    # prints departament information
    # and then build the list of disciplines that each departament have
    for index, departament in enumerate(campus.departments):

        async_tasks.append(
            (
                t_pool.apply_async(departament_scanner, (departament,)),
                index + 1
            )
        )

    for x in async_tasks:

        x[0].wait()

        print(
            "[Disciplines] Departament Progress: {} of {} ({}%)".format(
                x[1],
                departments_len,
                round(x[1]*100/departments_len, 2)
            ))

    return all_disciplines


if __name__ == '__main__':
    try:

        t_pool = ThreadPool(processes=4)

        # creates a campus object, it will hold
        # information about the campi on the Matricula Web
        campus = Campus()

        # call methodes to scrap courses and departaments information
        # frow the Web
        list_all_campus_courses = t_pool.apply_async(
            campus.getAllCampusCourses)
        list_all_campus_departments = t_pool.apply_async(
            campus.getAllCampusDepartments)

        list_all_campus_courses = list_all_campus_courses.get()
        list_all_campus_departments = list_all_campus_departments.get()

        # get habilitations and disciplines
        list_all_habilitations = t_pool.apply_async(
            proccessHabilitations, (campus, ))
        list_all_disciplines = t_pool.apply_async(
            proccessDisciplines, (campus, ))

        list_all_habilitations = list_all_habilitations.get()
        list_all_disciplines = list_all_disciplines.get()

        print(list_all_campus_courses)
        print(list_all_campus_departments)
        print(list_all_disciplines)
        print(list_all_habilitations)

    except KeyboardInterrupt:
        print('Interruption')
