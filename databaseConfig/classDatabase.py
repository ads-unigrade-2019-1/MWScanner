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
            {'code': class_object.getDepartment()})

        # Get all the attributes and insert in collection Mongodb
        collection_classes.insert_one({
            'name': class_object.getName(),
            'vacancies': class_object.getVacancies(),
            'discipline': class_object.getDiscipline(),
            'meetings': class_object.getMettings(),
            'shift': class_object.getShift(),
            'teachers': class_object.getTeachers(),
            'campus': department['campus']
        })
