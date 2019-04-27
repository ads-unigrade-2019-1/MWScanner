from databaseConfig.dbConnection import Database
from databaseConfig.classDatabase import ClassDb


class DisciplineDb(Database):
# This class is responsable for get all the 
# disciplines and save it in Mongodb

    @staticmethod
    def saveDiscipline(disciplines):

        # Get the instance of MongoDb
        db = Database.defineConnections()
        collection_discipline = db['disciplines']

        # Run all the disciplines list
        progress, total = 0, len(disciplines) - 1
        for discipline in disciplines:

            classes = []

            # Get all the classes from the current discipline
            if len(discipline.classes) >= 1:
                classes = [x.name for x in discipline.classes]
            
            # send the attributes with a dict to MongoDb
            collection_discipline.insert_one({
                'name': discipline.name,
                'code': discipline.code,
                'department': discipline.department,
                'classes': classes,
                'requirements': discipline.requirements,
                'credits': discipline.credits
            })

            # After save the disciplines call the method to
            # save the class 
            for c in discipline.classes:
                ClassDb.saveClass(c)

            progress += 1
            print("Saving disciplines and classes ({})...".format(
                (progress*100)/total))
