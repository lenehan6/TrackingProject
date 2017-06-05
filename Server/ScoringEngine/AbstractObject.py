from PyQt5.QtCore import *

from enum import *


class Type(Enum):
    Nil = 0;
    GapTime = 1;


class ScoringEngine_AbstractObject(QObject):
    resultReady = pyqtSignal('PyQt_PyObject');
    def __init__(self, type=Type.Nil, contest=None, parent=None):
        QObject.__init__(self, parent);
        self.updateInterval = -1;
        self.type = type;
        self.name = "";
        self._quit = False;
        self.contest = contest;
        self.db = "";

        self.workerThread = QThread();
        self.workerThread.start();
        self.moveToThread( self.workerThread );

    def start(self):
        QTimer.singleShot(0, self.run);

    @pyqtSlot()
    def run(self):
        self.timerEvent( QTimerEvent );
        self.startTimer( self.updateInterval );

    def setDatabase(self, db):
        self.db = db;

    def setUpdateInterval(self, tick):
        self.updateInterval = tick;
        if ( tick == -1 ):
            self.killTimer();
        else:
            self.startTimer( tick );

