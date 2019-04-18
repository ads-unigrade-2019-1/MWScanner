from databaseConfig.dbConnection import Database

class DisciplineDb(Database):

    @staticmethod
    def saveDiscipline(campus):

        db = Database.defineConnections()
        collection_discipline = db['disciplines']

        for departament in campus.departments:

            departament.buildLinkList()

            for discipline in departament.disciplines:
                for d in discipline:
                    
                    classes_list = []
                    
                    for classes in d.classes:
                        classes_list.append(classes.name)

                    collection_discipline.insert_one({
                        'name': d.name,
                        'code': d.code,
                        'departament': departament.code,
                        'classes': classes_list,
                        'requirements': d.requirements
                    })

                    
                        

               
                
    