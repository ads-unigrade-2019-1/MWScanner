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
            if len(discipline.getClasses()) >= 1:
                classes = [x.getName() for x in discipline.getClasses()]

            # send the attributes with a dict to MongoDb
            collection_discipline.insert_one({
                'name': discipline.getName(),
                'code': discipline.getCode(),
                'department': discipline.getDepartment(),
                'classes': classes,
                'requirements': discipline.getRequirements(),
                'credits': discipline.getCredits()
            })

            # After save the disciplines call the method to
            # save the class
            for c in discipline.getClasses():
                ClassDb.saveClass(c)

            progress += 1
            print("Saving disciplines and classes ({})...".format(
                (progress*100)/total))
