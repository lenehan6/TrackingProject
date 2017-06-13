from EventServer import WebServer
from time import sleep
from subprocess import call




#define
NOTIFY_CMD = "aws sns publish --topic-arn arn:aws:sns:ap-southeast-2:002508106093:SysAdmin --message ";
notify_count = 1;


def notify( www ):
    if (notify_count > 5):
        return;

    message = "Event Server down, restarting. Attempt #" + str(notify_count);
    if (notify_count == 5):
        message += ". No longer notifying SysAdmin...";

    print "Notifying SysAdmin";
    print NOTIFY_CMD + message;
    call([ (NOTIFY_CMD + message) ], shell=True);

while True:
    print "Start Distribution Server."
    www = WebServer();
    www.start();

    while www.isAlive():
        time.sleep(1);

    notify( www );
    print "Restarting Distribution Server..."

    time.sleep(1);

