## -------------------------
## Client ligne de commande
## -------------------------

# Permet de controler un agent

import sys
from multiprocessing.connection import Client
import time
import ConfigParser
import io

from job import Job
import cmd
import pdb

params = {}

default_config = """
[TEST_AGENT]
SERVEUR = localhost
PORT = 6000
PASSWORD = secret password
"""


def set_params(params):
    config = ConfigParser.RawConfigParser()
    config.readfp(io.BytesIO(default_config))
    params['SERVEUR'] = config.get('TEST_AGENT', 'SERVEUR')
    params['PORT'] = config.getint('TEST_AGENT', 'PORT')
    params['PASSWORD'] = config.get('TEST_AGENT', 'PASSWORD')

class SimpleClient(cmd.Cmd):
    """Simple command processor example."""
       
    def cmdloop(self, intro=None):
        #print 'cmdloop(%s)' % intro
        return cmd.Cmd.cmdloop(self, intro)
    
    ## ------------------------
    ## Effectue une connexion
    ## ------------------------
    ## Le parametre serveur est pour plus tard
    def conn(self, serveur=None):
        address = (params['SERVEUR'], params['PORT'])
        print "Connecting : ", address
        print "Params = ", params
        try:
            conn = Client(address, authkey=params['PASSWORD'])
            print "Connexion etablie"
            ## Reception de l'invite du serveur
            print conn.recv()
            return conn
        except:
            print "Erreur connexion"
            return None

    ## ------------------------------
    ## envoi un shutdown au serveur
    ## ------------------------------
    def do_shutdown(self, line):
        conn = self.conn()
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
        conn = self.conn()
        if conn:
            conn.send('list')
            print "Srv => ", conn.recv() # Nb process
            p = conn.recv()
            for l in p:
                print l
        conn=None

    ## --------------------------
    ## Envoi d'un job au serveur
    ## --------------------------
    def do_job(self, line):
        conn = self.conn()
        if conn:
            #print "Line = %s" % line
            r = cmd.Cmd.parseline(self, line)
            print "job = " , r
            if r[0] and r[1]:
                print "Sending JOB : %s" % r[0]
                conn.send('job')
                ## On doit recevoir  Ok send your job
                print "Srv => ", conn.recv()
                j=Job()
                j.name=r[0]
                j.cmd=r[1]
                conn.send(j)
                ## On doit recevoir Job receiveing ou erreur "
                print "Srv => ", conn.recv()
                ## On doit recevoir Job job finish"
                print "Srv => ", conn.recv()
                ## On doit recevoir le job
                j = conn.recv()
                ## On doit recevoir Invite de fin OK see your soon"
                print "Srv => ", conn.recv()
                ## la connexion doit se terminer
                ## Affichage du resultat
                j.pr()
            else:
                print "Job incorrecte [%s] [%s]" % (r[0], r[1])
        else:
            print "Not connected"
        ## Dans tout les cas la connexion est ferme
        conn=None

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
        print "See you soon ... "
        return True

    ## Pour exemple
    def do_greet(self, line):
        print "hello"

if __name__ == '__main__':
    pdb.set_trace()
    set_params(params)
    SimpleClient().cmdloop("Bienvenue ...")
