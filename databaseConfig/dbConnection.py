from pymongo import MongoClient
from databaseConfig.classDatabase import ClassDb
from databaseConfig.coursesDatabase import CourseDb
from databaseConfig.departamentDatabase import DepartamentDB
from databaseConfig.disciplineDatabase import DisciplineDb
from databaseConfig.habilitationDatabase import HabilitationDb

class Database:

    @staticmethod
    def defineConnections():
        client = MongoClient('mongodb://localhost:27017/')
        db = client['matriculaweb']
        return db

    @staticmethod
    def saveData(campus):
        ClassDb.saveClass(campus)
        CourseDb.saveCourses(campus)
        DepartamentDB.saveDepartament(campus)
        DisciplineDb.saveDiscipline(campus)
        HabilitationDb.saveHabilitation(campus)
