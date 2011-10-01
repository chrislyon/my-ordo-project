from multiprocessing.connection import Listener
from array import array

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey='secret password')

SHUTDOWN=False

print "Starting Listener "

while not SHUTDOWN:
    conn = listener.accept()
    print 'connection accepted from', listener.last_accepted
    conn.send('Here is the server waiting for cmd ...')
    cmd = conn.recv()
    print "cmd=%s" % cmd
    if cmd == "shutdown":
        SHUTDOWN = True
    conn.send('Ok see you soon')
    conn.close()

##
listener.close()
print "Ending prog"
