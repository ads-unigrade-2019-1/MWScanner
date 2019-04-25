from databaseConfig.dbConnection import Database


class departmentDB(Database):

    @staticmethod
    def savedepartment(departments):

        # db = self.defineConnections
        db = Database.defineConnections()
        collection_department = db['departments']

        old_size_list = 0

        for campus, department_list in departments.items():

            print("Saving departments for campus {}...".format(campus))

            size_list = len(department_list) - 1

            department_set = department_list[old_size_list: size_list]

            old_size_list = size_list

            for department in department_set:

                current_department = {
                    'campus': department.campus,
                    'code': department.code,
                    'name': department.name,
                    'initials': department.initials,
                    'disciplines': [x.code for x in department.disciplines]
                }

                collection_department.insert_one(current_department)
