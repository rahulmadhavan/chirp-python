import socket
import json
import threading
from chirp import Chirp,ChirpEncoder


MCAST_GRP = '224.1.1.4'
MCAST_PORT = 9292

_PUBlISH = "PUBLISH"
_STOP = "STOP"
_DISCOVER = "DISCOVER"

class ChirpBroadcaster():

    def __init__(self,_chirp_manager):
        self.chirp_manager  = _chirp_manager

    def broadcast(self,msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(msg, (MCAST_GRP, MCAST_PORT))

    def broadcast_chirp(self,chirp):
        message = json.dumps(chirp, cls = ChirpEncoder)
        self.broadcast(message)

    def publish(self):
        chirp = Chirp(_PUBlISH,
                        self.chirp_manager.name,
                        self.chirp_manager.uri,
                        self.chirp_manager.port,
                        self.chirp_manager.protocol)
        self.broadcast_chirp(chirp)

    def shutdown(self):
        chirp = Chirp(_STOP,self.chirp_manager.name)
        self.broadcast_chirp(chirp)

    def discover(self,name = ''):
        chirp = Chirp(_DISCOVER,name,_sender= self.chirp_manager.name)
        print str(threading.current_thread().ident) + ' broadcasting --  '+ json.dumps(chirp, cls = ChirpEncoder)
        self.broadcast_chirp(chirp)


