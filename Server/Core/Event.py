from PyQt5.QtCore import *
from Course import *

class Contest(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent);
        self.location = tuple();        # tuple with LANG/LONG
        self.courseFileLocation = '';   # save location of course KML
        self.course = '';               # KML object with course
        self.leader = '';
        self.db = '';

    def setDatabase(self, db):
        self.db = db;

    def setLocation(self, location):
        self.location = tuple(location);

    def setCourse(self, courseFileLocation):
        self.courseFileLocation = courseFileLocation;
        self.course = Course(courseFileLocation, self.db);

    def getSaveData(self):
        saveData["location"] = self.location;
        saveData["course"] = self.course;
        saveData["leader"] = self.leader;
        return saveData;
