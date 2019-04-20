from databaseConfig.dbConnection import Database


class CourseDb(Database):

    @staticmethod
    def saveCourses(courses):

        db = Database.defineConnections()
        collection_course = db['courses']

        for campus, course_list in courses.items():

            print("Saving courses for campus {}...".format(campus))

            for course in course_list:
                current_course = {
                    'code': course.code,
                    'campus': course.campus,
                    'name': course.name,
                    'shift': course.shift,
                    'modality': course.modality,
                    'habilitations': [x.code for x in course.habilitations]
                }

                collection_course.insert_one(current_course)
