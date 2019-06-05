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

        dict_disciplines = {}
        
        for discipline in disciplines:
            if discipline.getCode() in dict_disciplines:
                old_classes = dict_disciplines[discipline.getCode()].getClasses()
                dict_disciplines[discipline.getCode()].setClasses(old_classes + discipline.getClasses())              
            else:
                dict_disciplines[discipline.getCode()] = discipline
           

        progress, total = 0, len(dict_disciplines) - 1
        for discipline in dict_disciplines:

            classes = []

            # Get all the classes from the current discipline
            if len(dict_disciplines[discipline].getClasses()) >= 1:
                classes = [x.getName() for x in dict_disciplines[discipline].getClasses()]

            # send the attributes with a dict to MongoDb
            collection_discipline.insert_one({
                'name': dict_disciplines[discipline].getName(),
                'code': dict_disciplines[discipline].getCode(),
                'department': dict_disciplines[discipline].getDepartment(),
                'classes': classes,
                'requirements': dict_disciplines[discipline].getRequirements(),
                'credits': dict_disciplines[discipline].getCredits()
            })

            # After save the disciplines call the method to
            # save the class
            for c in dict_disciplines[discipline].getClasses():
                ClassDb.saveClass(c)

            progress += 1
            print("Saving disciplines and classes ({})...".format(
                (progress*100)/total))
