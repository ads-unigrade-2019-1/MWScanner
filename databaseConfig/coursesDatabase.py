from databaseConfig.dbConnection import Database


class CourseDb(Database):

    @staticmethod
    def saveCourses(campus):

        #db = self.defineConnections
        db = Database.defineConnections()
        collection_course = db['courses']

        for course in campus.courses:

            current_course = {}
            habilitation_list = []

            for habilitation in course.habilitations :
                habilitation_list.append(habilitation.code)

            current_course.update({
                'code': course.code,
                'campus': course.campus,
                'name': course.name,
                'shift': course.shift,
                'modality': course.modality,
                'habilitation': habilitation_list
            })

            collection_course.insert_one(current_course)
    