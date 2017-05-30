from PyQt4.QtCore import *
from PyQt4.QtSql import *
import time
import Location

class App( QObject ):
    def __init__(self, parent=None):
        QObject.__init__(self, parent);
        self.contest = '';
        self.webServer = '';
        self.scoringEngine = '';
        self.devices = [];
        #for writing to db directly
        self.db = QSqlDatabase.addDatabase("QPSQL");
        self.db.setHostName("localhost");
        self.db.setPort(5432);
        self.db.setDatabaseName("events");
        self.db.open();

        ##App should run in main thread - if it needs to run in another thread, commend the below back in.
        # self.workerThread = QThread( None );
        # self.workerThread.start();
        #
        # self.moveToThread( self.workerThread );

    def __del__(self):
        self.wait();

    def setContest(self, contest):
        self.contest = contest;

    def addDevice(self, device):
        self.devices.append( device );
        self.connect(device, SIGNAL("simulatorOutput(PyQt_PyObject)"), self.writeLocationToDb);

    def setWebServer(self, webServer):
        self.webServer = webServer;

    def setScoringEngine(self, engine):
        self.scoringEngine = engine;

    def writeLocationToDb( self, loc ):
        print loc.addr, " - Writing location", loc;
        query = "INSERT INTO stage1.gpsLocations (mac, time, serverTime, latitude, longitude, altitude, speed, direction) VALUES ( '" + loc.addr + "', " + str(loc.time) + ", " + str(loc.serverTime) + ", " + str(loc.latitude) + ", " + str(loc.longitude) + ", " + str(loc.altitude) + ", " + str(loc.velocity) + ", " + str(loc.vTheta) + ")";
        q = QSqlQuery(self.db);
        q.exec_(query);
        if q.lastError().type() != QSqlError.NoError:
            print "writeLocationToDb() $ query failed, ", q.lastError().text(), q.lastQuery();

        self.emit( SIGNAL("dbLocationsUpdated()") );
        return;

    def deleteEventData( self ):
        print "Deleting event data";
        query = "DELETE FROM stage1.gpsLocations";
        q = QSqlQuery(self.db);
        q.exec_(query);
        if q.lastError().type() != QSqlError.NoError:
            print "writeLocationToDb() $ query failed, ", q.lastError().text(), q.lastQuery();

        self.emit( SIGNAL("dbLocationsUpdated()") );
        return;



