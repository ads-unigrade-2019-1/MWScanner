from databaseConfig.dbConnection import Database


class CourseDb(Database):

    @staticmethod
    def saveCourses(courses):

        db = Database.defineConnections()
        collection_course = db['courses']

        old_size_list = 0

        for campus, course_list in courses.items():

            print("Saving courses for campus {}...".format(campus))

            size_list = len(course_list) - 1

            courses_set = course_list[old_size_list: size_list] 

            old_size_list = size_list
            
            for course in courses_set:
                
                current_course = {
                    'code': course.code,
                    'campus': course.campus,
                    'name': course.name,
                    'shift': course.shift,
                    'modality': course.modality,
                    'habilitations': [x.code for x in course.habilitations]
                }
    
                collection_course.insert_one(current_course)
