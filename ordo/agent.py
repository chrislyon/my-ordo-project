#!  /usr/bin/python
# -*- coding: UTF8 -*-
##----------------------------------------------------
## Projet        :  ordo
## Version       :  Alpha 0.0
## Auteur        :  chris
## Date Creation :  13/09/2011 11:36:15
## Objet         : agent.py
## MAJ           : 
## Bug Report    : 
## Todo List     : 
##----------------------------------------------------
## $Id :$
##----------------------------------------------------
## (c)  chris 2011
##----------------------------------------------------

## ---------------------------------------------
## Origine multiservice.py => Twisted Book
##
## Modifie par chris Sept 2011
##
## ---------------------------------------------
"""
    Composant Agent 
"""
## ----------------------------------------
## Issue des exemples de multiprocessing
## ----------------------------------------

from multiprocessing.connection import Listener
from array import array
import logging

from  worker import Worker
from job import Job

def log(msg):
    print ">>> %s " %  msg

SHUTDOWN=False
PASSWORD='secret password'
PORT=6000

log ("Starting listener")

address = ('', PORT)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=PASSWORD)

while not SHUTDOWN:
    conn = listener.accept()
    log ('connection accepted from %s '  % str(listener.last_accepted))
    conn.send('Here is the server waiting for cmd ...')
    cmd = conn.recv()
    log( "cmd=%s" % cmd)
    if cmd == "shutdown":
        SHUTDOWN = True
        conn.send("shutdown transmitted")
    elif cmd == "job":
        conn.send("Ok send your job")
        j = conn.recv()
        if isinstance(j, Job):
            w = Worker(j)
            w.work()
            conn.send(j)
    conn.send('Ok see you soon')
    conn.close()

##
listener.close()
log( "Ending prog" )
