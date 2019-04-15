from databaseConfig.dbConnection import Database


class ClassDb(Database):

    @staticmethod
    def saveClass(campus):

        db = Database.defineConnections()
        collection_classes = db['classes']

        for departament in campus.departments:

            departament.buildLinkList()

            for discipline in departament.disciplines:

                for d in discipline: 

                    for classe in d.classes:

                        collection_classes.insert_one({
                            'name': classe.name,
                            'vacancies': classe.vacancies,
                            'discipline': classe.discipline.code,
                            'meetings': classe.meetings,
                            'shift': classe.shift,
                            'teachers': classe.teachers
                        })
                    
    