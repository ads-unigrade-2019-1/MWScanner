class Campus():
    # This class represent all the 4 campus prensent in UnB

    # Define the attributes basics from all campus
    def __init__(self):

        self.__all_campus_courses = {}
        self.__courses = []

        self.__all_campus_departments = {}
        self.__departments = []

    def getAllCampusCourses(self):
        return self.__all_campus_courses

    def setAllCampusCourses(self, campus_courses):
        if isinstance(campus_courses, type(self.__all_campus_courses)):
            self.__all_campus_courses = campus_courses

    def getCourses(self):
        return self.__courses

    def setCourses(self, courses):
        if isinstance(courses, type(self.__courses)):
            self.__courses = courses

    def getAllCampusDepartments(self):
        return self.__all_campus_departments

    def setAllCampusDepartments(self, campus_departments):
        if isinstance(campus_departments, type(self.__all_campus_departments)):
            self.__all_campus_departments = campus_departments

    def getDepartments(self):
        return self.__departments

    def setDepartments(self, departments):
        if isinstance(departments, type(self.__departments)):
            self.__departments = departments
    
