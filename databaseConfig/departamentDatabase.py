from databaseConfig.dbConnection import Database
from mwscanner.Discipline import Discipline


class DepartamentDB(Database):

    @staticmethod
    def saveDepartament(campus):

        #db = self.defineConnections
        db = Database.defineConnections()
        collection_departament = db['departaments']

        for departament in campus.departments:
            current_departament = {}

            departament.buildLinkList()

            list_disciplines = []

            for unprocessed_disclipline in departament.unprocessedDisciplines:

                list_disciplines.append(unprocessed_disclipline['Código'])

            current_departament.update({
                'campus': departament.campus,
                'code': departament.code,
                'name': departament.name,
                'initials': departament.initials,
                'disciplines': list_disciplines
            })

            collection_departament.insert_one(current_departament)
    