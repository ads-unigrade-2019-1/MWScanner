from databaseConfig.dbConnection import Database


class HabilitationDb(Database):

    @staticmethod
    def saveHabilitation(campus):

        # db = self.defineConnections
        db = Database.defineConnections()
        collection_habilitation = db['habilitations']

        for course in campus.courses:
            for habilitation in course.habilitations:
                current_habilitation = {}
                disciplines_list = []

                habilitation.buildLinkList()

                for key in habilitation.disciplines:
                    discipline_by_peorid = []

                    for discipline in habilitation.disciplines[key]:
                        discipline_by_peorid.append(discipline['Código'])
                    
                    disciplines_list.append({ key: discipline_by_peorid})

                current_habilitation.update({
                    'code': habilitation.code,
                    'name': habilitation.name + " (" + habilitation.degree + ")",
                    'disciplines': disciplines_list
                })

                collection_habilitation.insert_one(current_habilitation)

    
