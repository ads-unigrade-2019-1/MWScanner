from databaseConfig.dbConnection import Database


class DisciplineDb(Database):

    @staticmethod
    def saveDiscipline(campus):

        db = Database.defineConnections()
        collection_discipline = db['disciplines']

        for departament in campus.departments:

            departament.buildLinkList()

            current_discipline = {}

            for discipline in departament.disciplines:

                classes_list = []
                requeriments_list = []

                for classe in discipline.classes:
                    classes_list.append(classe.name)

                for requirement in discipline.requeriments:
                    requeriments_list.append(requirement.code)

                current_discipline.update({
                    'name': discipline.name,
                    'code': discipline.code,
                    'departament': departament.code,
                    'classe': classes_list,
                    'requeriments': requeriments_list
                })

                collection_discipline.insert_one(current_discipline)
                
    