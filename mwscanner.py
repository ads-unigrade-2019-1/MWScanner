import sys

from multiprocessing.pool import ThreadPool

from mwscanner.builders.CampusBuilder import CampusBuilder
from mwscanner.Campus import Campus
from mwscanner.Discipline import Discipline
from databaseConfig.SaveData import SaveData


BASE_URL = 'https://matriculaweb.unb.br/'


def proccessHabilitations(campus: Campus):

    all_habilitations = []

    t_pool = ThreadPool(processes=8)
    async_tasks = []

    courses_len = len(campus.getCourses())

    for index, course in enumerate(campus.getCourses()):

        for habilitation in course.habilitations:

            all_habilitations.append(habilitation) 

            '''print(
                "[HABILITATIONS] Course Progress: {} of {} ({}%)".format(
                    x[1],
                    courses_len,
                    round(x[1]*100/courses_len, 2)
                ))'''

    return all_habilitations


def proccessDisciplines(campus: Campus):

    all_disciplines = []

    t_pool = ThreadPool(processes=16)
    async_tasks = []

    departments_len = len(campus.getDepartments())

    # prints department information
    # and then build the list of disciplines that each department have
    for index, department in enumerate(campus.getDepartments()):

        async_tasks.append(
            (
                t_pool.apply_async(department.buildFromHtml),
                index + 1
            )
        )

    for x in async_tasks:

        department = x[0].get()

        if len(department.disciplines) > 0:
            for d in department.disciplines:
                all_disciplines.append(d)

        print(
            "[Disciplines] department Progress: {} of {} ({}%)".format(
                x[1],
                departments_len,
                round(x[1]*100/departments_len, 2)
            ))

    t_pool.terminate()
    return all_disciplines


if __name__ == '__main__':

    try:

        t_pool = ThreadPool(processes=2)

        # creates a campus object, it will hold
        # information about the campi on the Matricula Web
        campus = CampusBuilder().buildCampus()
        
        # call methodes to scrap courses and departments information
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

        t_pool.terminate()

        print(list_all_disciplines)

        print("Calling db save function...")

        SaveData.saveData(
            list_all_campus_courses,
            list_all_campus_departments,
            list_all_habilitations,
            list_all_disciplines
        )

    except KeyboardInterrupt:
        print('Interruption')
