from PyQt4.QtCore import *
from Core.Location import Location

from enum import *


class ScoringEngine_GapTimeEngine( ScoringEngine_AbstractObject ):
    def __init__(self, contest, parent=None):
        super( self, ScoringEngine_GapTimeEngine).__init__(self, Type.GapTime, contest, parent);
        #manually update every 5 seconds
        self.setUpdateInterval( 5 );
        #for writing to db directly
        self.db = QSqlDatabase.addDatabase("QPSQL", str(time.time()));
        self.db.setDatabaseName("db");
        self.db.open();

        if ~( db.isOpen() ):
            raise AttributeError( "Database connection could not be established" );

        #end __init__

    def timerEvent(self, event):
        return self.calculateCurrentGap();


    def lastLocations(self):
        locs = list();
        leader = "";

        query = "SELECT p.mac, p.time, p.longitude, p.latitude, p.altitude FROM (SELECT MAX(id) as id, mac FROM stage1.gpsLocations GROUP BY mac) m JOIN stage1.gpsLocations p ON m.id = p.id";
        q = QSqlQuery(self.db);
        q.exec_(query);
        while ( q.next() ):
            loc = Location();
            addr = q.value("mac").toString();
            loc.setAddress( addr );
            loc.setPosition( q.value("longitude").toInt(),
                             q.value("latitude").toInt(),
                             q.value("altitude").toInt()
                             );
            loc.setTime( q.value("time").toInt() );
            locs.append( loc );
            if addr == self.contest.leader:
                leader = loc;

        return leader, locs;

    def calculateCurrentGap(self):

        leader, locations = self.lastLocations();

        query = "SELECT * gpsLocations (mac, time, serverTime, latitude, longitude, altitude, speed, direction) VALUES ( '" + loc.addr + "', " + str(loc.time) + ", " + str(loc.serverTime) + ", " + str(loc.latitude) + ", " + str(loc.longitude) + ", " + str(loc.altitude) + ", " + str(loc.velocity) + ", " + str(loc.vTheta) + ")";
        q = QSqlQuery(self.db);
        q.exec_(query);

        return;






