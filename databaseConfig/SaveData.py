from databaseConfig.coursesDatabase import CourseDb
from databaseConfig.departmentDatabase import DepartmentDB
from databaseConfig.disciplineDatabase import DisciplineDb
from databaseConfig.habilitationDatabase import HabilitationDb
from databaseConfig.dbConnection import Database

from multiprocessing.pool import ThreadPool


class SaveData:
    # This is only a class intermediate between extraction part
    # and mongoDb

    @staticmethod
    def saveData(courses, departments, habilitations, disciplines):
        # This method get all the list come from extraction part
        # and call the respective function for manipulate and send
        # the data to database

        db = Database.defineConnections()

        # Remove all the data in collections
        # before the save
        db['classes'].remove({})
        db['courses'].remove({})
        db['departments'].remove({})
        db['disciplines'].remove({})
        db['habilitations'].remove({})

        print('Saving to DB...')

        print('Saving courses...')
        CourseDb.saveCourses(courses)

        print('Saving departments...')
        DepartmentDB.savedepartment(departments)

        print('Saving disciplines and classes...')
        DisciplineDb.saveDiscipline(disciplines)

        print('Saving habilitations...')
        HabilitationDb.saveHabilitation(habilitations)

        print("Wrinting to db done")
