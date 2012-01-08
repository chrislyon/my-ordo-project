#! /usr/bin/python
## -------------------------
## Client ligne de commande
## -------------------------

# Permet de controler un agent
# 

# ajout de batch
# mais le batch n'est pas mis a jour quand
# le job revient de l'agent

## pour l'instant un seul agent
## pas de bdd pour les jobs

##
## Quelques ordres : 
##
## list         : list les jobs de l'agent 
## job          : envoi un job a l'agent : job NOM COMMANDE
## batch        : envoi un batch a l'agent : batch NOM COMMANDE
## blist        : liste l'etat des batchs
## bpr          : rapport pour chaque batchs
## shutdown     : arret de l'agent
## show         : liste les parametres
## quit         : sortie

from multiprocessing.connection import Client
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
import ConfigParser
import io

from job import Job
from job_list import JobList
import cmd
import pdb

## Les parametres
params = {}

default_config = """
[TEST_AGENT]
SERVEUR = localhost
PORT = 6000
PASSWORD = secret password
"""


## ---------------------
## Lancement d'un batch
## dans un process
## ---------------------
def run_batch(batch, conn, b_list):
    """ Lance un job en batch """
    #print "Sending BATCH : %s" % batch
    conn.send('job')
    ## On doit recevoir  Ok send your job
    msg = conn.recv()
    conn.send(batch)
    ## On doit recevoir Job receiveing ou erreur "
    msg = conn.recv()
    ## On doit recevoir Job job finish"
    msg = conn.recv()
    ## On doit recevoir le job
    ret = conn.recv()
    #print ret.pr()
    b_list.add(ret)
    ## On doit recevoir Invite de fin OK see your soon"
    msg = conn.recv()
    ## la connexion doit se terminer
    conn = None

def set_params(params):
    """ Pour l'instant defini les parametres """
    config = ConfigParser.RawConfigParser()
    config.readfp(io.BytesIO(default_config))
    params['SERVEUR'] = config.get('TEST_AGENT', 'SERVEUR')
    params['PORT'] = config.getint('TEST_AGENT', 'PORT')
    params['PASSWORD'] = config.get('TEST_AGENT', 'PASSWORD')

class MyManager(BaseManager):
    pass

MyManager.register('BList', JobList)

class SimpleClient(cmd.Cmd):
    """Simple command processor example."""
     
    ## -----------------------------
    ## Declarations des Managers
    ## -----------------------------
    manager = MyManager()
    manager.start()
    b_list = manager.BList()

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
        conn = None


    ## ----------------------------------
    ## Envoi d'un batch / job au serveur
    ## ----------------------------------
    def do_batch(self, line):
        #print "Line = %s" % line
        r = cmd.Cmd.parseline(self, line)
        #print "job = " , r
        if r[0] and r[1]:
            conn = self.conn()
            ## la il faut passer la main
            ## a process
            j = Job()
            j.name = r[0]
            j.cmd = r[1]
            b = Process(target=run_batch, args=(j,conn,self.b_list))
            b.start()
        else:
            print "Job incorrecte [%s] [%s]" % (r[0], r[1])

   ## -------------------------
   ## Liste des batchs
   ## -------------------------
    def do_blist(self, line):
        """ Liste des batchs """
        #for k,j in self.b_list.items():
        #    print "k=%s j=%s" % (k,j)
        self.b_list.pr()

    def do_bpr(self, line):
        """ Etat des batchs """
        self.b_list.pr(line)

    ## ----------------------------------------
    ## Affichage des parametres de connexion
    ## ----------------------------------------
    def do_show(self, line):
        """ montre les parametres """
        for k, v in params.items():
            print "%-20s - %-20s" % (k,v)
       
    ## sortie de la ligne de commande
    def do_quit(self,line):
        """ Sortie de la ligne de commande """
        return self.do_EOF(line)
   
    def do_EOF(self, line):
        """ Fin du bal ... """
        print "See you soon ... "
        return True

    def emptyline(self):
        pass

    ## Pour exemple
    def do_greet(self, line):
        """ Say Hello """
        print "hello"

if __name__ == '__main__':
    #pdb.set_trace()
    set_params(params)
    SimpleClient().cmdloop("Bienvenue ...")

