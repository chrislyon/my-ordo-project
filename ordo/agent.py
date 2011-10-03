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
from multiprocessing import Process, Queue
import multiprocessing
import logging

from array import array
import time

from  worker import Worker
from job import Job

## ---------------------------
##  Execution d'une commande
## ---------------------------
def do_request( conn ):
    conn.send("Ok send your job")
    j = conn.recv()
    if isinstance(j, Job):
        w = Worker(j)
        w.work()
        conn.send(j)
    conn.send('Ok see you soon')
    conn.close()

## ---------------------------
## MAIN
## ---------------------------

logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)

SHUTDOWN=False
PASSWORD='secret password'
PORT=6000

logger.info ("Starting listener")

address = ('', PORT)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=PASSWORD)

p_list = []

while not SHUTDOWN:
    conn = listener.accept()
    logger.info ('connection accepted from %s '  % str(listener.last_accepted))
    conn.send('Here is the server waiting for cmd ...')
    cmd = conn.recv()
    logger.info( "cmd=%s" % cmd)
    if cmd == "shutdown":
        SHUTDOWN = True
        conn.send("shutdown transmitted")
        time.sleep(5)
        conn.close()
    elif cmd == "list":
        conn.send("liste")
        conn.close()
    elif cmd == "job":
        p = Process(target=do_request, args=(conn,))
        p_list.append(p)
        p.start()
##
listener.close()
logger.info( "Ending prog" )
