from pymongo import MongoClient
import re
import mwscanner

#Connect to database

client = MongoClient('mongodb://localhost:27017/')
db = client['mwtest']
colCourse = db['course']
colDisciplines = db['discipline']
colHabilitation = db['habilitation']
colDepartament = db['departament']


def save_data(campus):

    list_disciplines = []
    list_habilitations = []
    list_course = []
    list_departaments = []

    
    for course in campus.courses:

        list_course.append(course)
        
        for habilitation in course.habilitations:
            habilitation.buildLinkList()
            list_habilitations.append(habilitation)

    save_habilitations(list_habilitations)
        
            
    '''
    for departament in campus.departments:
            departament.buildLinkList()
            list_disciplines.append({ departament.name: departament.disciplines})
            #list_departaments.append(departament)
    save_all_disciplines(list_disciplines)
    '''


def save_all_disciplines(disciplines):
    for sub_discipline in disciplines:
        for key in sub_discipline:    
            for single_discipline in sub_discipline[key]:
                current_discipline = {}
                current_discipline.update({
                    'code' : single_discipline['Código'],
                    'name': single_discipline['Denominação'],
                    'departament': key
                })
                colDisciplines.insert_one(single_discipline)

def save_habilitations(habilitations):

    for habilitation in habilitations:

        current_habilitation = {}
        diciplines_by_period = []
    
        for periods in habilitation.disciplines:

            list_disciplines = []
            current_period = re.search(r'\d+',periods['Período']).group()

            for discipline in periods['Disciplinas']:
                list_disciplines.append(discipline['Código'])
            diciplines_by_period.append({
                current_period: list_disciplines
            })
            
                
        current_habilitation.update({
            'name': habilitation.name + " (" + habilitation.degree + ")",
            'code': habilitation.code,
            'disciplines': diciplines_by_period
        })
        
        colHabilitation.insert_one(current_habilitation)
        
def save_courses(courses):

    for course in courses:

        list_habilitations = []
        dict_course = {}

        for habilitation in course.habilitations:
            list_habilitations.append(habilitation.code)
        
        dict_course.update({
            'campus': course.campus,
            'code': course.code,
            'name': course.name,
            'shift': course.shift,
            'modality': course.shift,
            'habilitations': list_habilitations
        })

        colCourse.insert_one(dict_course)    

def save_departament(departaments):

    for departament in departaments:

        list_disciplines = []
        current_departament = {}

        for disciplines in departament.disciplines:
            list_disciplines.append(disciplines['Código'])

        current_departament.update({
            'campus': departament.campus,
            'code': departament.code,
            'name':  departament.name,
            'initials': departament.initials,
            'disciplines': list_disciplines
        })

        colDepartament.insert_one(current_departament)





        

