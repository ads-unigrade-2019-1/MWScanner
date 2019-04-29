from databaseConfig.dbConnection import Database


class ClassDb(Database):
    # This class get all the classes Objects and save it in MongoDb

    @staticmethod
    def saveClass(class_object):
        # This method get the list of classes from disciplines
        # and save it like a document in MongoDb collection

        # To instantiate the connection with MongoDb
        # Call the collections class and department
        db = Database.defineConnections()
        collection_classes = db['classes']
        collection_departments = db['departments']

        # Get the class campus belonged
        department = collection_departments.find_one(
            {'code': class_object.department})

        # Get all the attributes and insert in collection Mongodb
        collection_classes.insert_one({
            'name': class_object.name,
            'vacancies': class_object.vacancies,
            'discipline': class_object.discipline.code,
            'meetings': class_object.meetings,
            'shift': class_object.shift,
            'teachers': class_object.teachers,
            'campus': department['campus']
        })
