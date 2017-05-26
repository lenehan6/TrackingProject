from PyQt4.QtCore import *
from Course import *

class Contest(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent);
        self.location = tuple();        # tuple with LANG/LONG
        self.courseFileLocation = '';   # save location of course KML
        self.course = '';               # KML object with course
        self.leader = '';


    def setLocation(self, location):
        self.location = tuple(location);

    def setCourse(self, courseFileLocation):
        self.courseFileLocation = courseFileLocation;
        self.course = Course(courseFileLocation);

    def getSaveData(self):
        saveData["location"] = self.location;
        saveData["course"] = self.course;
        saveData["leader"] = self.leader;
        return saveData;
