from PyQt5.QtCore import *
from PyQt5.QtSql import *

from Database import Database
import time
import Location

class App( QObject ):
    dbLocationsUpdated = pyqtSignal();
    def __init__(self, parent=None):
        qDebug( "new App() object" );
        super( App, self ).__init__(parent);
        self.contest = '';
        self.webServer = '';
        self.scoringEngine = '';
        self.devices = [];
        self.groups = [];
        #for writing to db directly
        self.db = "";

        ##App should run in main thread - if it needs to run in another thread, commend the below back in.
        # self.workerThread = QThread( None );
        # self.workerThread.start();
        #
        # self.moveToThread( self.workerThread );

    def setContest(self, contest):
        self.contest = contest;

    def addDevice(self, device):
        self.devices.append( device );
        device.simulatorOutput.connect( self.writeLocationToDb );
        #self.connect(device, SIGNAL("simulatorOutput(PyQt_PyObject)"), self.writeLocationToDb);

    def addGroup(self, group):
        self.groups.append( group );

    def setWebServer(self, webServer):
        self.webServer = webServer;

    def setScoringEngine(self, engine):
        self.scoringEngine = engine;
        engine.resultReady.connect( self.updateGapTimes );

    def setDatabase( self, db ):
        self.db = db;

    @pyqtSlot('PyQt_PyObject')
    def writeLocationToDb( self, loc ):
        # qDebug( "App.writeLocationToDb()" );
        tick = time.time();
        #print loc.addr, " - Writing location", loc;
        query = "INSERT INTO stage1.gpsLocations (mac, time, serverTime, latitude, longitude, altitude, speed, direction, distance) VALUES ( '" + loc.addr + "', " + str(loc.time) + ", " + str(loc.serverTime) + ", " + str(loc.latitude) + ", " + str(loc.longitude) + ", " + str(loc.altitude) + ", " + str(loc.velocity) + ", " + str(loc.vTheta) + ", " + str(loc.distance) + ")";
        q = self.db.do_query( query );
        if q.lastError().type() != QSqlError.NoError:
            print "writeLocationToDb() $ query failed, ", q.lastError().text(), q.lastQuery();

        self.dbLocationsUpdated.emit();
        tock = time.time() - tick;
        if ( tock > 0.2 ):
            qWarning( "WARNING! writeLocationToDb() took " + str( int(tock*1000) ) + "ms" );

        return;

    @pyqtSlot('PyQt_PyObject')
    def updateGapTimes(self, gapTimes):
        #qDebug( "updateGapTimes(), gapTimes==" + gapTimes.__repr__() );
        for d in self.devices:
            if d.addr in gapTimes:
                d.setGapTime( gapTimes[ d.addr ] );

    def getDeviceById(self, id):
        for d in self.devices:
            if ( d.id == id ):
                return d;

        return None;

    def deleteEventData( self ):
        qDebug( "App.deleteEventData()" );
        query = "DELETE FROM stage1.gpsLocations";
        q = self.db.do_query( query );
        if q.lastError().type() != QSqlError.NoError:
            print "writeLocationToDb() $ query failed, ", q.lastError().text(), q.lastQuery();


        # self.emit( SIGNAL("dbLocationsUpdated()") );
        return;



