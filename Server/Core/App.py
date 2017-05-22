import threading

class App( threading.Thread ):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super(App, self).__init__(group, target, name, args, kwargs);
        self.event = '';
        self.webServer = '';
        self.devices = [];
        self.start();

    def setEvent(self, event):
        self.event = event;

    def addDevice(self, device):
        self.devices.append( device );

    def setWebServer(self, webServer):
        self.webServer = webServer;

