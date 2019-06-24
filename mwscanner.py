from multiprocessing.pool import ThreadPool

from mwscanner.builders.CampusBuilder import CampusBuilder
from mwscanner.Campus import Campus
from databaseConfig.SaveData import SaveData


BASE_URL = 'https://matriculaweb.unb.br/'


def proccessHabilitations(campus: Campus):

    all_habilitations = []

    for index, course in enumerate(campus.getCourses()):

        for habilitation in course.getHabilitations():

            all_habilitations.append(habilitation) 

    return all_habilitations


def proccessDisciplines(campus: Campus):

    all_disciplines = []

    # prints department information
    # and then build the list of disciplines that each department have
    for index, department in enumerate(campus.getDepartments()):

        for discipline in department.getDisciplines():
            
            all_disciplines.append(discipline)
      
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

        print("Calling db save function...")

        SaveData.saveData(
            list_all_campus_courses,
            list_all_campus_departments,
            list_all_habilitations,
            list_all_disciplines
        )

    except KeyboardInterrupt:
        print('Interruption')
