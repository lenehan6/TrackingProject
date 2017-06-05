from PyQt5.QtCore import *
from PyQt5.QtSql import *
import Database
import json

class Group( QObject ):
    _id = 0;
    gapTimeChanged = pyqtSignal( float );
    def __init__(self, app):
        super( Group, self ).__init__();
        self.db = app.db;
        self.app = app;

        self.id = Group._id;
        self.name = "Group";
        self.gap = -1;
        self.bibs = list();
        self.deviceId = -1;

        self.device = '';
        self.conn_gapTime = None;
        Group._id += 1;
        self.save();

    def __dict__(self):
        d = dict();
        d["id"]     = self.id;
        d["name"]   = self.name;
        d["gap"]    = self.gap;
        d["bibs"]   = self.bibs;
        d["deviceId"] = self.deviceId;
        return d;

    def save(self):
        query = "INSERT INTO stage1.settings (key, value) VALUES ('Group/1', '" + json.dumps( self.__dict__() ) + "') ON CONFLICT (key) DO UPDATE SET value='" + json.dumps( self.__dict__() ) + "'";
        q = self.db.do_query(query);
        if q.lastError().type() != QSqlError.NoError:
            qDebug(q.lastError().text() + " (" + q.lastQuery() + ")");
        return;

    def setDevice(self, device):
        self.device = device;
        self.deviceId = device.id;

        if ( self.conn_gapTime != None ):
            self.conn_gapTime.disconnect();

        self.conn_gapTime = device.gapTimeChanged.connect( self.updateGapTime );

    @pyqtSlot(float)
    def updateGapTime(self, gap):
        qDebug( "updateGapTime(), gap==" + str(gap) );
        self.gap = gap;
        self.gapTimeChanged.emit( gap );

    def setName(self, name):
        self.name = name;








