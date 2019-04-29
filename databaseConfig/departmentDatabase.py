from databaseConfig.dbConnection import Database


class DepartmentDB(Database):
    # This class was created to save all the departments
    # present in UnB

    @staticmethod
    def savedepartment(departments):
        # This static method the department list and save
        # it in database Mongodb

        # Get the instance from database connection
        db = Database.defineConnections()
        collection_department = db['departments']

        old_size_list = 0

        # Run for all the department list
        for campus, department_list in departments.items():

            print("Saving departments for campus {}...".format(campus))

            # How it comes with the entire list having all the departaments,
            # we split the list according with the campus
            size_list = len(department_list)

            department_set = department_list[old_size_list: size_list]

            old_size_list = size_list

            # After the split get the current attributes and
            # save all of then in Mongo
            for department in department_set:

                current_department = {
                    'campus': department.campus,
                    'code': department.code,
                    'name': department.name,
                    'initials': department.initials,
                    'disciplines': [x.code for x in department.disciplines]
                }

                collection_department.insert_one(current_department)
