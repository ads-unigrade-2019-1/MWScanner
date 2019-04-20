from databaseConfig.dbConnection import Database


class departmentDB(Database):

    @staticmethod
    def savedepartment(departments):

        #db = self.defineConnections
        db = Database.defineConnections()
        collection_department = db['departments']

        for campus, department_list in departments.items():

            print("Saving departments for campus {}...".format(campus))

            for department in department_list:

                current_department = {
                    'campus': department.campus,
                    'code': department.code,
                    'name': department.name,
                    'initials': department.initials,
                    'disciplines': [x.code for x in department.disciplines]
                }

                collection_department.insert_one(current_department)
