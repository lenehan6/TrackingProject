from PyQt4.QtCore import *

from enum import *


class Type(Enum):
    Nil = 0;
    Simulator = 1;


class IODevice_AbstractObject(QObject):
    def __init__(self, contest, type=Type.Nil, parent=None):
        QThread.__init__(self, parent);
        self.updateInterval = -1;
        self.type = type;
        self.contest = contest;
        self.name = ""
        self._quit = False;
        self.addr = "";
        self.workerThread = QThread();
        self.workerThread.start();
        self.moveToThread( self.workerThread );

    def __del__(self):
        self.workerThread.quit();
        self.workerThread.wait();

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