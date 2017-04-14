from threading import Thread

from Course import Course


class Event(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super(Event, self).__init__(group, target, name, args, kwargs);
        self.location = tuple();        # tuple with LANG/LONG
        self.courseFileLocation = '';   # save location of course KML
        self.course = '';               # KML object with course


    def setLocation(self, location):
        self.location = tuple(location);

    def setCourse(self, courseFileLocation):
        self.courseFileLocation = courseFileLocation;
        self.course = Course(courseFileLocation);

    def getSaveData(self):
        saveData["location"] = self.location;
        saveData["course"] = self.course;
        return saveData;
