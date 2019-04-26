from databaseConfig.dbConnection import Database
from databaseConfig.classDatabase import ClassDb


class DisciplineDb(Database):

    @staticmethod
    def saveDiscipline(disciplines):

        db = Database.defineConnections()
        collection_discipline = db['disciplines']

        progress, total = 0, len(disciplines) - 1
        for discipline in disciplines:

            classes = []

            if len(discipline.classes) >= 1:
                classes = [x.name for x in discipline.classes]

            collection_discipline.insert_one({
                'name': discipline.name,
                'code': discipline.code,
                'department': discipline.department,
                'classes': classes,
                'requirements': discipline.requirements,
                'credits': discipline.credits
            })

            for c in discipline.classes:
                ClassDb.saveClass(c)

            progress += 1
            print("Saving disciplines and classes ({})...".format(
                (progress*100)/total))
