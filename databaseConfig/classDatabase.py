from databaseConfig.dbConnection import Database


class ClassDb(Database):

    @staticmethod
    def saveClass(campus):

        db = Database.defineConnections()
        collection_discipline = db['classes']

        for departament in campus.departments:

            departament.buildLinkList()

            for discipline in departament.disciplines:

                for classe in discipline.classes:

                    collection_discipline.insert_one(classe)
                
    