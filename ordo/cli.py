## -------------------------------------------
## Client de base pour transmettre des infos
## aux composants
## -------------------------------------------

import sys
from multiprocessing.connection import Client
import time

from job import Job
import pdb

SERVEUR='localhost'
PORT=6000
PASSWORD='secret password'
address = (SERVEUR, PORT)
conn = Client(address, authkey=PASSWORD)

print conn.recv()   # Entete du serveur

if len(sys.argv) > 1 :
    cmd=sys.argv[1]
    if cmd == 'j1':
        print "Cli : JOB1"
        conn.send('job')
        print "Srv => ", conn.recv()
        j=Job()
        j.name='TYPE JOB 1'
        j.cmd="ls -l ; sleep 55"
        #j.cmd="ls -l "
        conn.send(j)
        j = conn.recv()
        j.pr()
        conn.close()
    elif cmd == 'j2':
        print "Cli : JOB2"
        conn.send('job')
        print "Srv => ", conn.recv()
        j=Job()
        j.name='TYPE JOB 2'
        j.cmd="ls -l ; sleep 25"
        #j.cmd="ls -l "
        conn.send(j)
        j = conn.recv()
        j.pr()
        conn.close()
    else:
        print "Sending ... %s " % cmd
        conn.send(cmd)
        print "Srv => ", conn.recv()
        conn.close()
else:
    #pdb.set_trace()
    print "Cli => liste"
    conn.send('list')
    print "Srv => ", conn.recv() # Nb process
    p = conn.recv()
    for l in p:
        print l
    conn.close()


