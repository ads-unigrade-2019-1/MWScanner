
class Habilitation():
    def __init__(self):
        self.__code = ""
        self.__name = ""
        self.__degree = ""

        # This represents the disciplines associated with this
        # course. The data here wiil be on the following format:
        # disciplines = {
        #   'PERIOD_NUMBER': [list with the code for the
        #                     discipline of this period]
        #   ...
        # }
        self.__disciplines = {}

    def getCode(self):
        return self.__code

    def getName(self):
        return self.__name

    def getDegree(self):
        return self.__degree

    def getDisciplines(self):
        return self.__disciplines

    def setCode(self, code):
        if isinstance(code, type(self.__code)):
            self.__code = code

    def setName(self, name):
        if isinstance(name, type(self.__name)):
            self.__name = name
    
    def setDegree(self, degree):
        if isinstance(degree, type(degree)):
            self.__degree = degree

    def setDisciplines(self, disciplines):
        if isinstance(disciplines, type(self.__disciplines)):
            self.__disciplines = disciplines

