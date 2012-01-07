
## -------------------------
## Client ligne de commande
## -------------------------

# Permet de controler un agent

# ajout de batch
# mais le batch n'est pas mis a jour quand
# le job revient de l'agent

import sys
from multiprocessing.connection import Client
from multiprocessing import Process, Queue, Manager
import time
import ConfigParser
import io

from job import Job
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
## ---------------------
def run_batch(batch, conn, cle):
       print "Sending BATCH : %s" % batch
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
       print ret.pr()
       b_list.append( ret )
       ## On doit recevoir Invite de fin OK see your soon"
       msg = conn.recv()
       ## la connexion doit se terminer
       conn=None

def set_params(params):
   config = ConfigParser.RawConfigParser()
   config.readfp(io.BytesIO(default_config))
   params['SERVEUR'] = config.get('TEST_AGENT', 'SERVEUR')
   params['PORT'] = config.getint('TEST_AGENT', 'PORT')
   params['PASSWORD'] = config.get('TEST_AGENT', 'PASSWORD')

## -----------------------------
## Declarations des Managers
## -----------------------------
manager = Manager()
b_list = manager.list()

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
           j=Job()
           j.name=r[0]
           j.cmd=r[1]
           b = Process(target=run_batch, args=(j,conn,j.name))

           b.start()
       else:
           print "Job incorrecte [%s] [%s]" % (r[0], r[1])

   ##
   ##
   ##
   def do_blist(self, line):
       for b,j in b_list:
           print "B=%s j=%s" % (b,j)

   def do_bpr(self, line):
       for b in b_list:

           print "Job : %s " % b
           b.pr()

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
   #pdb.set_trace()
   set_params(params)
   Manager = MyManager()
   Manager.start()
   SimpleClient().cmdloop("Bienvenue ...")

