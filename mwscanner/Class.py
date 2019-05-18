class Class():
    # This class represents a discipline class on Matricula
    # Web. It contains data about the meetings and a
    # connection to the discipline.

    def __init__(self):

        # name of class, example: "Turma A"
        # this is unique inside a discipline
        self.__name = ''

        # number of available vacancies in this class
        self.__vacancies = 0

        # discipline in which this class belongs
        self.__discipline = ""

        # a meeting should have the structure:
        # {
        #   room: str
        #   day: str
        #   hour: str
        # }
        self.__meetings = []
        self.__shift = ''

        # teachers is a list
        self.__teachers = []

        # campus from subject
        self.__department = ""

    def getName(self):
        return self.__name

    def setName(self, name):
        if isinstance(name, type(self.__name)):
            self.__name = name

    def getVacancies(self):
        return self.__vacancies

    def setVacancies(self, vacancies):
        if isinstance(vacancies, type(self.__vacancies)):
            self.__vacancies = vacancies

    def getDiscipline(self):
        return self.__discipline

    def setDiscipline(self, discipline):
        if isinstance(discipline, type(self.__discipline)):
            self.__discipline = discipline

    def getMettings(self):
        return self.__meetings

    def setMettings(self, meetings):
        if isinstance(meetings, type(self.__meetings)):
            self.__meetings = meetings

    def getShift(self):
        return self.__shift

    def setShift(self, shift):
        if isinstance(shift, type(self.__shift)):
            self.__shift = shift
    
    def getTeachers(self):
        return self.__teachers

    def setTeachers(self, teachers):
        if isinstance(teachers, type(self.__teachers)):
            self.__teachers = teachers

    def getDepartment(self):
        return self.__department

    def setDepartment(self, department):
        if isinstance(department, type(self.__department)):
            self.__department = department