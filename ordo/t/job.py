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
        print "Start date      : %s " % self.start_date.strftime("%x %X %f")
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

