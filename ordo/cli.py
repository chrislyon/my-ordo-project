
import sys
from multiprocessing.connection import Client
from array import array

from job import Job

address = ('localhost', 6000)
conn = Client(address, authkey='secret password')

print conn.recv()   # Entete du serveur

if len(sys.argv) > 1 :
    conn.send(sys.argv[1])
    print "Srv => ", conn.recv()
else:
    print "Cli => job"
    conn.send('job')
    print "Srv => ", conn.recv()
    j=Job()
    j.name='TEST'
    j.cmd="ls -l"
    conn.send(j)
    j = conn.recv()
    j.pr()

print conn.recv()   # Entete du serveur

conn.close()
