import threading,socket,struct,time,json
from chirp import ChirpDecoder

MCAST_GRP = '224.1.1.4'
MCAST_PORT = 9292


class ChirpReceiver(threading.Thread):

    def __init__(self,_chirp_manager):
        super(ChirpReceiver,self).__init__()
        self._stopping = False
        self._pause = 5
        self.chirp_manager = _chirp_manager

    def run(self):
        print "chirp listener about to listen to chirps"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((MCAST_GRP, MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while not self._stopping:
            msg = sock.recv(10240)
            try:
                chirp = json.loads(msg,cls=ChirpDecoder)
            except Exception as e:
                print "---------------------------------"
                print "message could not be interpreted"
                print e.message
                print "---------------------------------"
            self.chirp_manager.notify(chirp)
            time.sleep(self._pause)


    def stop(self):
        self._stopping = True

