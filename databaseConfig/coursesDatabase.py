from databaseConfig.dbConnection import Database


class CourseDb(Database):
    #  This class get the list of courses in some campus
    # from UnB and save it in MongoDb

    @staticmethod
    def saveCourses(courses):
        # This method static get the list of courses and
        # save it in MongoDb

        # Instantiate the database connection and
        # create get the collection course from Mongo
        db = Database.defineConnections()
        collection_course = db['courses']

        old_size_list = 0

        # Run through the course lists
        for campus, course_list in courses.items():

            print("Saving courses for campus {}...".format(campus))

            size_list = len(course_list)

            # How it comes with the entire list having all the departaments,
            # we split the list according with the campus
            courses_set = course_list[old_size_list: size_list]

            old_size_list = size_list

            # Get all the attributes from the current course
            # Save it in mongo collection
            for course in courses_set:

                current_course = {
                    'code': course.code,
                    'campus': course.campus,
                    'name': course.name,
                    'shift': course.shift,
                    'modality': course.modality,
                    'habilitations': [str(x.getCode()) for x in course.habilitations]
                }

                collection_course.insert_one(current_course)
