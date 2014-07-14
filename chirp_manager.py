import json
import time
import threading
from chirp import ChirpEncoder
import chirp_broadcaster
import chirp_receiver




_PUBlISH = "PUBLISH"
_STOP = "STOP"
_DISCOVER = "DISCOVER"

class ChirpManager():

    def __init__(self,_name,_port,_protocol,_uri,_config={}):
        self.name = _name
        self.port = _port
        self.protocol = _protocol
        self.uri = _uri
        self.config = _config
        self.chirpers = {}
        self.chirp_broadcaster = chirp_broadcaster.ChirpBroadcaster(self)
        self.chirp_receiver = chirp_receiver.ChirpReceiver(self)
        self.chirp_receiver.setDaemon(True)

    def details(self):
        return {'name': self.name,
                'port': self.port,
                'uri': self.uri,
                'protocol': self.protocol,
                'config': self.config}


    def add_chirper(self,chirp):
        self.chirpers[chirp.name] ={'name': chirp.name,
                                    'port': chirp.port,
                                    'uri':chirp.uri,
                                    'protocol':chirp.protocol,
                                    'config':chirp.config}

    def remove_chirper(self,chirp):
        del self.chirpers[chirp.name]

    def notify(self,chirp):
        if chirp.sender != self.name:
            print str(threading.current_thread().ident) + ' notified -- ' + json.dumps(chirp,cls=ChirpEncoder)
            if chirp.method == _PUBlISH:
                self.add_chirper(chirp)
            elif chirp.method == _STOP:
                self.remove_chirper(chirp.name)
            elif chirp.method == _DISCOVER:
                if chirp.name.strip() == '':
                    self.chirp_broadcaster.publish()
                elif chirp.name.strip() == self.name:
                    self.chirp_broadcaster.publish()
            else:
                print "This bird doesn't know how to chirp"
                print json.loads(chirp,cls=ChirpEncoder)


    def stop(self):
        self.chirp_receiver.stop();


    def list_chirpers(self):
        return self.chirpers.keys()

    def fetch_no_wait(self,chirper_name):
        if chirper_name in self.chirpers:
            return True,self.chirpers[chirper_name]
        else:
            self.chirp_broadcaster.discover(chirper_name)
            return False,""

    def fetch(self,chirper_name):
        if chirper_name.strip() == self.name:
            print 'fetching current chirper ' + chirper_name
            return self.details()
        elif chirper_name in self.chirpers:
            print 'fetching existing chirper ' + chirper_name
            return self.chirpers[chirper_name]
        else:
            self.chirp_broadcaster.discover(chirper_name)
            print 'fetching chirper ' + chirper_name
            count = 10
            while count < 10:
                if chirper_name in self.chirpers:
                    print 'chirper found ' + chirper_name
                    return self.chirpers[chirper_name]
                    return self.chirpers[chirper_name]
                else:
                    time.sleep(1)
                    count = count + 1
            return False

    def start_chirping(self):
        self.chirp_receiver.start()
        self.chirp_broadcaster.publish()
        self.chirp_broadcaster.discover()


# def main():
#     cm = ChirpManager(sys.argv[1],9200,'http','chirp.org')
#     cm.start_chirping()
#
#     while True:
#         try:
#             time.sleep(10)
#         except KeyboardInterrupt:
#             cm.stop()
#             break
#
#
# if __name__ == '__main__':
#     main()
#
