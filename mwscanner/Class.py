
class Class():
    # This class represents a discipline class on Matricula
    # Web. It contains data about the meetings and a
    # connection to the discipline.

    def __init__(self, name, vacancies, discipline, meetings, teachers):

        # name of class, example: "Turma A"
        # this is unique inside a discipline
        self.name = name

        # number of available vacancies in this class
        self.vacancies = vacancies

        # discipline in which this class belongs
        self.discipline = discipline

        # a meeting should have the structure:
        # {
        #   room: str
        #   day: str
        #   hour: str
        # }
        self.meetings = meetings

        self.teachers = teachers

    # def appendMeeting(self, room, day, init_hour, final_hour):
    #     # adds a meeting to this class list of meetings
    #     # all parameters are strings
    #     # room: room where the meeting will occour
    #     # day: weekday of the meeting
    #     # hour: time of the meeting

    #     self.meetings.append({
    #         'day': day,
    #         'init_hour': init_hour,
    #         'final_hour': final_hour,
    #         'room': room
    #     })
