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

import elixir
import model
from model import *

from job import Job
from job_list import JobList
import cmd
import pdb

## Les parametres
params = {}

metadata = elixir.metadata

default_config = """
[TEST]
DB_FILE = db/data_ordo.sqlite
"""


## ----------------------------
## definition des parametres
## ----------------------------
def set_params(params):
    """ Pour l'instant defini les parametres """
    print "Reading parameters "
    config = ConfigParser.RawConfigParser()
    config.readfp(io.BytesIO(default_config))
    params['DB_FILE'] = config.get('TEST', 'DB_FILE')

## ----------------------
## Mise en route BDD
## ----------------------
def setup_db(meta):
    datafile = params['DB_FILE']
    print "Using database : %s " % datafile
    meta.bind = "sqlite:///"+datafile

    meta.bind.echo = True
    meta.bind.echo = False

    elixir.setup_all()
    
def setup_default(params):
    print "setting default parameters"
    a = model.Agent.query.filter_by(default_agent = True).one()
    if a :
        params['DEFAULT_AGENT'] = a
        print "Default agent = %s " % a 
    else:
        print "No default agent set ..."

### ---------------------------------------------
### Le manager sert a gerer les objets transmis
### ---------------------------------------------
class MyManager(BaseManager):
    pass

MyManager.register('BList', JobList)


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
    ## Envoi du job
    conn.send(batch)
    ## On doit recevoir Job receiveing ou erreur "
    msg = conn.recv()
    ## On doit recevoir Job job finish"
    msg = conn.recv()
    ## On doit recevoir le job
    ret = conn.recv()
    if isinstance(ret, Job):
        print ret.pr()
        b_list.add(ret)
        ## On doit recevoir finish result
        msg = conn.recv()
    else:
        print "Not a job : %s " % ret
    ## On doit recevoir Invite de fin OK see your soon"
    msg = conn.recv()
    ## la connexion doit se terminer
    conn = None


## --------------------------
## Client ligne de commande
## --------------------------
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
        agent = params['DEFAULT_AGENT']
        print "Mot de passe <%s>" % agent.password
        address = (agent.server_ip, agent.server_port)
        print "Connecting : ", address
        print "Params = ", params
        try:
            ## important le str(agent.password) est necessaire
            ## sinon pas reconnu
            conn = Client(address, authkey=str(agent.password))
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
    def do_list(self, line):
        #print "Line = %s" % line
        r = cmd.Cmd.parseline(self, line)
        sub = r[0]

        if sub == 'process':
            conn = self.conn()
            if conn:
                conn.send('list')
                print "Srv => ", conn.recv() # Nb process
                p = conn.recv()
                for l in p:
                    print l
            conn=None
        elif sub == 'agent':
            for ag in Agent.query.all():
                print ag
        else:
            print "Inconnue : %s / %s" % (sub, r)

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
                ## On doit recevoir Job job finish sending result"
                print "Srv => ", conn.recv()
                ## On doit recevoir le job
                j = conn.recv()
                ## On doit recevoir result transmit
                print "Srv => ", conn.recv()
                ## On doit recevoir Invite de fin OK see your soon"
                print "Srv => ", conn.recv()
                ## la connexion doit se terminer
                ## Affichage du resultat
                if isinstance(j, Job):
                    j.pr()
                else:
                    print "Not a job %s " % j
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
        try:
            self.b_list.pr(line)
        except:
            print "Batch %s inexistant ..." % line

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

    def do_test(self, line):
        print "Line = %s" % line
        r = cmd.Cmd.parseline(self, line)
        print r
        

    ## Pour exemple
    def do_greet(self, line):
        """ Say Hello """
        print "hello"

if __name__ == '__main__':
    #pdb.set_trace()
    set_params(params)
    setup_db(metadata)
    setup_default(params)
    SimpleClient().cmdloop("Bienvenue ...")

