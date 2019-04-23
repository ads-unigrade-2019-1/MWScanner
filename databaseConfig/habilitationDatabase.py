from databaseConfig.dbConnection import Database


class HabilitationDb(Database):

    @staticmethod
    def saveHabilitation(habilitations):

        db = Database.defineConnections()
        collection_habilitation = db['habilitations']

        progress, total = 0, len(habilitations) - 1
        for habilitation in habilitations:
            disciplines_list = []

            for period, disciplines in habilitation.disciplines.items():
                disciplines_list.append(
                    {period: [d['Código'] for d in disciplines]})

            current_habilitation = {
                'code': habilitation.code,
                'name': habilitation.name + " (" + habilitation.degree + ")",
                'disciplines': disciplines_list
            }

            collection_habilitation.insert_one(current_habilitation)

            progress += 1
            print("Saving habilitations ({})...".format(
                (progress*100)/total))
