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
    ## Envoi d'un message d'invite
    logger.info("demarrage d'une requete")
    conn.send("Ok send your job")
    run = False
    logger.info("Attente du job")
    try:
        j = conn.recv()
        run = True
    except:
        logger.info("Probleme reception job")

    ## ya pas eu d'erreur 
    if run:
        logger.info("Reception du job %s " % j)
        if isinstance(j, Job):
            conn.send('Job receive')
            logger.info("Creation Worker")
            w = Worker(j)
            logger.info("Lancement Worker")
            w.work()
            logger.info("Worker fini")
            conn.send('Job finishsending result ')
            conn.send(j)
        conn.send('Ok see you soon')
        conn.close()
    else:
        logger.info("Erreur not a job %s " % j)
        conn.send('Error not a job')
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
    try:
        cmd = conn.recv()
    except EOFError:
        logger.info("Connexion ended by peer")
        conn.close()
        continue
        
    logger.info( "cmd=%s" % cmd)
    logger.info( "p=%s" % len(p_list))

    if cmd == "shutdown":
        SHUTDOWN = True
        conn.send("shutdown transmitted")
        time.sleep(3)
        conn.close()
    elif cmd == "list":
        conn.send("liste des processus en cours : %s " % len(p_list))
        l = []
        for p in p_list:
            l.append( (p.name, p.is_alive(), p.pid ) )
            logger.debug(p.name, p.is_alive(), p.pid )
        logger.info(l)
        conn.send(l)
        conn.close()
    elif cmd == "job":
        p = Process(target=do_request, args=(conn,))
        p_list.append(p)
        p.start()
    else:
        conn.send("Commande inconnue : %s" % cmd)
        conn.close()
##
listener.close()
logger.info( "Ending prog" )
