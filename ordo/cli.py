
import sys
from multiprocessing.connection import Client

from job import Job

address = ('localhost', 6000)
conn = Client(address, authkey='secret password')

print conn.recv()   # Entete du serveur

if len(sys.argv) > 1 :
    conn.send(sys.argv[1])
    print "Srv => ", conn.recv()
    conn.close()
else:
    print "Cli => job"
    conn.send('job')
    print "Srv => ", conn.recv()
    j=Job()
    j.name='TEST'
    j.cmd="ls -l ; sleep 5"
    #j.cmd="ls -l "
    conn.send(j)
    j = conn.recv()
    j.pr()
    conn.close()


