from threading import Thread

from enum import *


class Type(Enum):
    Nil = 0;
    Simulator = 1;


class IODevice_AbstractObject(Thread):
    def __init__(self, event, type=Type.Nil, group=None, target=None, name=None, args=(), kwargs={}):
        super(IODevice_AbstractObject, self).__init__(group, target, name, args, kwargs);
        self.updateInterval = -1;
        self.type = type;
        self.event = event;
        self.quit = False;

    def setUpdateInterval(self, interval):
        self.updateInterval = int(interval);

    def getSaveData_AbstractObject(self):
        saveData["type"] = self.type;
        saveData["updateInterval"] = self.updateInterval;
        return saveData;
