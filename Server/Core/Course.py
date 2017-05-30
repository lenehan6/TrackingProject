from Location import Location
import time

from PyQt4.QtCore import *
from PyQt4.QtSql import *

import xml.etree.ElementTree as ET
import re


class Course(QObject):
    def __init__(self, kmlFileLocation):
        QObject.__init__(self, None);
        self.length = 0;

        self.db = QSqlDatabase.addDatabase("QPSQL", "Course_" + str(time.time()));
        self.db.setHostName("localhost");
        self.db.setPort(5432);
        self.db.setDatabaseName("events");
        self.db.open();

        query = "DELETE FROM stage1.course";
        q = QSqlQuery(self.db);
        q.exec_(query);

        query = "DELETE FROM stage1.course2";
        q = QSqlQuery(self.db);
        q.exec_(query);

        with open(kmlFileLocation) as f:
            self.file = f.read();
            s = re.sub('<kml.+>', '<kml>', self.file);
            self.kml = ET.fromstringlist(s);
            s = str(self.kml.find(".//coordinates").text);

            values = [];

            self.coords = [];
            for line in s.split("\n"):
                line2 = line.split(",");
                if (len(line2) == 3):
                    wp = Location();
                    wp.setPosition(float(line2[0]), float(line2[1]), float(line2[2]));
                    self.coords.append(wp);
                    #values.append( "'POINT("+str(float(line2[0]))+" "+line2[1]+" "+line2[2]+")'::geometry" );
                    values.append( str(float(line2[0]))+" "+line2[1]+" "+line2[2] );

            #query = "INSERT INTO stage1.course (pos) VALUES (" + '), ('.join(values) + ")";
            query = "INSERT INTO stage1.course2 (sector, line) VALUES ( 1, 'LINESTRING(" + ', '.join(values) + ")'::geography )";
            q = QSqlQuery( self.db );
            q.exec_( query );

            query = "SELECT sector, ST_Length(line) as line_distance FROM stage1.course2";
            q = QSqlQuery(self.db);
            q.exec_(query);
            if ( q.lastError().type() == QSqlError.NoError ):
                print "Sector\t| Distance (km)"
                print "------------------------------------"
                sum = 0;
                while q.next():
                    dist = q.value("line_distance").toFloat()[0];
                    sum += dist;
                    print q.value("sector").toInt()[0], "\t\t| ", dist/1000

                print "------------------------------------"
                print "TOTAL\t| ", sum/1000

                self.length = sum;
        print "Course() initalised";





    def pointAlongCourse(self, dbConn, percentage):

        tick = time.time();
        if ( percentage > 1.0 ):
            print "percentage (", percentage, ") is greater than 1, returning"
            return Location();

        # if ~(dbConn.isOpen()):
        #     dbConn.open();
        #     print "db (", dbConn.connectionName(), ") is not open, attempted to open"


        query = "SELECT ST_AsText(ST_LineInterpolatePoint(line::geometry, " + str(percentage) + ")) as position FROM stage1.course2";
        #print query;
        q = QSqlQuery(dbConn);
        q.exec_(query);

        point = Location();

        if ( q.lastError().type() == QSqlError.NoError ):
            while q.next():
                result = q.value("position").toString();
                #print result;
                r = re.compile('[POINT Z ()]+')
                #print "regexp returns", r.split( result );
                coords = r.split( result );
                point.setPosition( coords[1].toFloat()[0], coords[2].toFloat()[0], coords[3].toFloat()[0]);
                break; #only looking for 1 result

        tock = time.time() - tick;
        if ( tock > 0.2 ):
            print "pointAlongCourse() took ", time.time() - tick, "seconds to return";

        return point;



    def getClosestPointToCoordinate(self, (long, lat, alt), lastId=-1):
        # if lastId == -1, search whole file for closest point. Include lastId for faster fix.
        return (long, lat, alt);
