from PyQt5.QtCore import *

from enum import *


class Type(Enum):
    Nil = 0;
    Simulator = 1;


class IODevice_AbstractObject(QObject):
    id = 0;

    gapTimeChanged = pyqtSignal(float);
    def __init__(self, contest, type=Type.Nil, parent=None):
        super( IODevice_AbstractObject, self ).__init__(parent);
        self.updateInterval = -1;
        self.type = type;
        self.contest = contest;
        self.name = "";
        self.label = "<Auto>";
        #<Auto> should generate label depending on members of group and position in race
        #e.g. "Leader", "Pursvant", "Sagan and 5 others", etc.
        self._quit = False;
        self.addr = "";
        self.db = '';
        self.isEnabled = True;
        self.distance = 0;
        self.speed = 0;
        self.id = IODevice_AbstractObject.id;
        self.gap = -1;
        IODevice_AbstractObject.id += 1;

    def getLabel(self):
        if self.label is not "<Auto>":
            return self.label;
        else:
            return "Group " + str(self.id);

    def setIsEnabled(self, isEnabled):
        self.isEnabled = isEnabled;

    def quit(self):
        self._quit = True;

    def setUpdateInterval(self, interval):
        self.updateInterval = int(interval);

    def getSaveData_AbstractObject(self):
        saveData["type"] = self.type;
        saveData["updateInterval"] = self.updateInterval;
        return saveData;

    def setDeviceName(self, name):
        self.name = name;

    def setDatabase(self, db):
        self.db = db;

    def setGapTime(self, gap):
        #qDebug( "setGapTime(), gap==" + str(gap) );
        self.gap = gap;
        self.gapTimeChanged.emit( gap );