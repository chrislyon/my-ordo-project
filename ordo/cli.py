## -------------------------
## Client ligne de commande
## -------------------------

import sys
from multiprocessing.connection import Client
import time

from job import Job
import cmd
import pdb

conn = None

params = {
    'SERVEUR' : 'localhost',
    'PORT' : 6000,
    'PASSWORD' : 'secret password'
}


class SimpleClient(cmd.Cmd):
    """Simple command processor example."""
       
    def cmdloop(self, intro=None):
        #print 'cmdloop(%s)' % intro
        return cmd.Cmd.cmdloop(self, intro)
    
    ## ------------------------
    ## Effectue une connexion
    ## ------------------------
    def do_conn(self,line):
        global conn
        address = (params['SERVEUR'], params['PORT'])
        try:
            conn = Client(address, authkey=params['PASSWORD'])
            print "Connexion etablie"
        except:
            print "Erreur connexion"
        ## Reception de l'invite du serveur
        print conn.recv()

    ## ------------------------------
    ## envoi un shutdown au serveur
    ## ------------------------------
    def do_shutdown(self, line):
        global conn
        if conn:
            conn.send("shutdown")
            conn.close()
            conn = None
        else:
            print "Not connected ..."

    ## --------------------------
    ## Liste des processes
    ## --------------------------
    def do_list(self,line):
        global conn
        if conn:
            conn.send('list')
            print "Srv => ", conn.recv() # Nb process
            p = conn.recv()
            for l in p:
                print l

    ## --------------------------
    ## Envoi d'un job au serveur
    ## --------------------------
    def do_job(self, line):
        global conn
        if conn:
            #print "Line = %s" % line
            r = cmd.Cmd.parseline(self, line)
            print "job = " , r
            if r[0] and r[1]:
                print "Sending JOB : %s" % r[0]
                conn.send('job')
                print "Srv => ", conn.recv()
                j=Job()
                j.name=r[0]
                j.cmd=r[1]
                conn.send(j)
                j = conn.recv()
                j.pr()
            else:
                print "Job incorrecte [%s] [%s]" % (ret[0], ret[1])
        else:
            print "Not connected"

    ## ----------------------------------------
    ## Affichage des parametres de connexion
    ## ----------------------------------------
    def do_show(self, line):
        for k, v in params.items():
            print "%-20s - %-20s" % (k,v)
        
    ## sortie de la ligne de commande
    def do_quit(self,line):
        return self.do_EOF(line)
    
    def do_EOF(self, line):
        if conn:
            conn.close()
            print "Closing Connexion ..."
        print "See you soon ... "
        return True

    ## Pour exemple
    def do_greet(self, line):
        print "hello"

if __name__ == '__main__':
    SimpleClient().cmdloop("Bienvenue ...")

### -------------------------------------------
### Client de base pour transmettre des infos
### aux composants
### -------------------------------------------
#
#import sys
#from multiprocessing.connection import Client
#import time
#
#from job import Job
#import pdb
#
#SERVEUR='localhost'
#PORT=6000
#PASSWORD='secret password'
#address = (SERVEUR, PORT)
#conn = Client(address, authkey=PASSWORD)
#
#print conn.recv()   # Entete du serveur
#
#if len(sys.argv) > 1 :
#    cmd=sys.argv[1]
#    if cmd == 'j1':
#        print "Cli : JOB1"
#        conn.send('job')
#        print "Srv => ", conn.recv()
#        j=Job()
#        j.name='TYPE JOB 1'
#        j.cmd="ls -l ; sleep 55"
#        #j.cmd="ls -l "
#        conn.send(j)
#        j = conn.recv()
#        j.pr()
#        conn.close()
#    elif cmd == 'j2':
#        print "Cli : JOB2"
#        conn.send('job')
#        print "Srv => ", conn.recv()
#        j=Job()
#        j.name='TYPE JOB 2'
#        j.cmd="ls -l ; sleep 25"
#        #j.cmd="ls -l "
#        conn.send(j)
#        j = conn.recv()
#        j.pr()
#        conn.close()
#    else:
#        print "Sending ... %s " % cmd
#        conn.send(cmd)
#        print "Srv => ", conn.recv()
#        conn.close()
#else:
#    #pdb.set_trace()
#    print "Cli => liste"
#    conn.send('list')
#    print "Srv => ", conn.recv() # Nb process
#    p = conn.recv()
#    for l in p:
#        print l
#    conn.close()
#
#
