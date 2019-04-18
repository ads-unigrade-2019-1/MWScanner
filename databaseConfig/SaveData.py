from databaseConfig.coursesDatabase import CourseDb
from databaseConfig.departamentDatabase import DepartamentDB
from databaseConfig.disciplineDatabase import DisciplineDb
from databaseConfig.habilitationDatabase import HabilitationDb
from databaseConfig.classDatabase import ClassDb

class SaveData:

    @staticmethod
    def saveData(campus):
        ClassDb.saveClass(campus)
        CourseDb.saveCourses(campus)
        DepartamentDB.saveDepartament(campus)
        DisciplineDb.saveDiscipline(campus)
        HabilitationDb.saveHabilitation(campus)