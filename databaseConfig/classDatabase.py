from databaseConfig.dbConnection import Database


class ClassDb(Database):

    @staticmethod
    def saveClass(class_object):

        db = Database.defineConnections()
        collection_classes = db['classes']
        collection_departments = db['departments']

        department = collection_departments.find_one({'code': class_object.department})

        collection_classes.insert_one({
            'name': class_object.name,
            'vacancies': class_object.vacancies,
            'discipline': class_object.discipline.code,
            'meetings': class_object.meetings,
            'shift': class_object.shift,
            'teachers': class_object.teachers,
            'campus': department['campus']
        })
