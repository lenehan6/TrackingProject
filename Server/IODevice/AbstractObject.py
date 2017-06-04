from PyQt5.QtCore import *

from enum import *


class Type(Enum):
    Nil = 0;
    Simulator = 1;


class IODevice_AbstractObject(QObject):
    def __init__(self, contest, type=Type.Nil, parent=None):
        super( IODevice_AbstractObject, self ).__init__(parent);
        self.updateInterval = -1;
        self.type = type;
        self.contest = contest;
        self.name = ""
        self._quit = False;
        self.addr = "";
        self.db = '';


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