import sys
from multiprocessing.connection import Client
from array import array

from job import Job

address = ('localhost', 6000)
conn = Client(address, authkey='secret password')

print conn.recv()   # Entete du serveur

if sys.argv[1]:
    conn.send(sys.argv[1])
else:
    j=Job()
    j.name='TEST'
    j.cmd="ls -l"
    conn.send(j)

print conn.recv()   # Entete du serveur

conn.close()
