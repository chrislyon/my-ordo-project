#!  /usr/bin/python
# -*- coding: UTF8 -*-
##----------------------------------------------------
## Projet        :  ordo
## Version       :  Alpha 0.0
## Auteur        :  chris
## Date Creation :  13/09/2011 11:36:15
## Objet         : job.py
## MAJ           : 
## Bug Report    : 
## Todo List     : 
##----------------------------------------------------
## $Id :$
##----------------------------------------------------
## (c)  chris 2011
##----------------------------------------------------

import yaml
import pdb

class Job(object):
    def __init__(self, name=None, cmd=None, args=None):

        ## Attributs identification
        self.name = name
        self.groupe = ""
        self.uniqid = 0

        ## Attributs commande
        self.cmd = cmd
        self.args = args

        ## Atributs execution
        self.status = "Initial"
        self.stderr = None
        self.stdout = None
        self.returncode = None
        self.ilog = []
        self.pid = None


        ## Attributs statistiques
        self.start_date = None
        self.end_date = None
    
    def pr(self):
        print "Resultat du job : %s " % self.name
        print "Commande        : %s " % self.cmd
        print "Args            : %s " % self.args
        print "Code de retour  : %s " % self.returncode
        print "Status          : %s " % self.status
        print "process ID      : %s " % self.pid
        if self.start_date:
            print "Start date      : %s " % self.start_date.strftime("%x %X %f")
        if self.end_date:
            print "end   date      : %s " % self.end_date.strftime("%x %X %f")
        print "-" * 40
        for i in self.ilog:
            print i
        print "-" * 40
        print self.stdout
        print "-" * 40
        print self.stderr
        print "-" * 40

    def __repr__(self):
        return "< %s %s %s >" % (self.name, self.status, self.returncode)

    def to_y(self):
        return yaml.dump(self)

    def from_y(self, y):
        self = yaml.load(y)
        return self


if __name__ == '__main__':
    pdb.set_trace()
    j = Job()
    j.name = "TOTO"
    j.cmd = "ls -l ; sleep 0"

    jy = j.to_y()

    j2 = yaml.load(jy)

    del j

    j = Job()
    j = j.from_y(jy)

    print jy
    print j2.pr()
    print j
    print j.pr()

