#!  /usr/bin/python
# -*- coding: UTF8 -*-
##----------------------------------------------------
## Projet        :  ordo
## Version       :  Alpha 0.0
## Auteur        :  chris
## Date Creation :  13/09/2011 11:36:15
## Objet         : worker.py
## MAJ           : 
## Bug Report    : 
## Todo List     : 
##----------------------------------------------------
## $Id :$
##----------------------------------------------------
## (c)  chris 2011
##----------------------------------------------------
import subprocess
import datetime
import job
import pdb

class Worker(object):
    def __init__(self, job=None):
        self.history = []
        self.job = job
        self.ilog = []

    def set_ilog(self, msg, typ="debug"):
        ts=datetime.datetime.now().strftime('%d.%m %X')
        self.ilog.append( "%s :%s: %s" % (ts, typ, msg) )

    def work(self):

        self.set_ilog("Demarrage")
        self.job.status = "Lancement du job"
        self.set_ilog("Ajout dans l'historique")
        self.history.append(self.job)
        self.set_ilog("Analyse du job")
        self.job.status = "Analyse"
        if self.job:
            self.set_ilog("Job present execution")
            self.job.start_date = datetime.datetime.now()
            self.job.status = "Execution"
            proc = subprocess.Popen(
                self.job.cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                )
            self.job.status = "Execution termine"
            self.set_ilog("Recuperation des resultats")
            (self.job.stdout, self.job.stderr) = proc.communicate()
            self.job.pid = proc.pid
            self.job.returncode = proc.returncode
            rc = proc.returncode
            self.job.status = "Mise a jour attribut "
            self.set_ilog("fin execution rc=%s" % rc)
        else:
            self.job.status = "Mise a jour attribut "
            set_ilog("job inexistant", typ='ERR' )
            rc = -1
        self.job.end_date = datetime.datetime.now()
        self.set_ilog("Fin ")
        self.job.status = "Fin du job - A retourner"
        self.job.ilog = self.ilog
        return rc


if __name__ == "__main__":

    #pdb.set_trace()

    j = job.Job()
    print "Job = ", j

    w = Worker(j)
    j.name = "test"
    j.cmd = "ls -l /etc"
    w.work()

    j.pr()


    
