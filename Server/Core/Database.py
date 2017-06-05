from PyQt5.QtCore import *
from PyQt5.QtSql import *

import time

class Database( QObject ):
    def __init__(self):
        # event handling in another thread....
        # self.workerThread = QThread();
        # self.workerThread.start();
        # self.moveToThread( workerThread );
        qDebug( "new Database() object" );
        self.mutex = QMutex();

        self.threads = dict();
        self.threads[ str(QThread.currentThread()) ] = self.newDatabase( "DatabaseObjectThread_" + str(time.time()) );

        qDebug("Database() initalised");

    def newDatabase(self, name):
        qDebug( "Database.newDatabase()" );
        db = QSqlDatabase.addDatabase("QPSQL", name);
        db.setHostName("localhost");
        db.setPort(5432);
        db.setDatabaseName("events");
        db.setConnectOptions("connect_timeout=2");
        db.open();

        return db;

    def do_query(self, query):
        # qDebug( "Database.do_query()");
        QMutexLocker( self.mutex );

        if str(QThread.currentThread()) not in self.threads:
            self.threads[ str(QThread.currentThread()) ] = self.newDatabase( str(QThread.currentThread()) + "_" + str(time.time()) );
            #qDebug( self.threads.__repr__() );

        db = self.threads[ str(QThread.currentThread()) ];

        if not db.isOpen():
            qWarning( str(QThread.currentThread()) + " database connection not open, attempting to reopen");
            if not db.open():
                qWarning(str(QThread.currentThread()) + " database connection failed!");

        q = QSqlQuery( db );
        q.exec_( query );

        return q;
