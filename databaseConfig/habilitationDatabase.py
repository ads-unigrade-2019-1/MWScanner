from databaseConfig.dbConnection import Database


class HabilitationDb(Database):
    # Class static to save all data related to
    # Habilitation in Courses
    @staticmethod
    def saveHabilitation(habilitations):
        # This method get the habilitations list, manipulate it
        # and insert in mongoDb

        #  Get the instance from database
        db = Database.defineConnections()
        collection_habilitation = db['habilitations']

        progress, total = 0, len(habilitations) - 1
        for habilitation in habilitations:
            disciplines_list = []

            # In all habilitation get the discipline code and add it in
            # list from all disciplines related to habilitation
            for period, disciplines in habilitation.getDisciplines().items():
                disciplines_list.append(
                    [[d['Código'], d['Nome']] for d in disciplines]
                )

            # Add the main attributes in dict create a consistent data
            current_habilitation = {
                'code': str(habilitation.getCode()),
                'name': habilitation.getName() + " (" + habilitation.getDegree() + ")",
                'disciplines': disciplines_list
            }

            # Insert it in collection of habilitations
            collection_habilitation.insert_one(current_habilitation)

            progress += 1
            print("Saving habilitations ({})...".format(
                (progress*100)/total))
