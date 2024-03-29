## ------------------------------
## Init de la base de donnees
## ------------------------------

import os
import datetime
from elixir import *

datafile = "db/data_ordo.sqlite"
metadata.bind = "sqlite:///"+datafile

metadata.bind.echo = True
metadata.bind.echo = False

class Agent(Entity):
    using_options(tablename='AGENT')
    name = Field(Unicode(30))
    description = Field(UnicodeText)
    server_ip = Field(Unicode(30))
    server_name = Field(Unicode(30))
    server_port = Field(Integer)

class Job(Entity):
    using_options(tablename='JOB')
    name = Field(Unicode(30))
    cmd = Field(UnicodeText)
    description = Field(UnicodeText)
    job_exec = OneToMany('JobExec')
    
    def __repr__(self):
        return '<Job "%s" (%d)>' % (self.name, self.cmd)

class JobExec(Entity):
    using_options(tablename='JOB_EXEC')
    job = ManyToOne('Job')
    status = Field(Integer)
    return_code = Field(Integer)
    stderr = Field(UnicodeText)
    sdtout = Field(UnicodeText)
    start_date = Field(DateTime)
    end_date = Field(DateTime)
    ex_log = OneToMany('ExecLog')

class ExecLog(Entity):
    using_options(tablename='EXEC_LOG')
    job_exec = ManyToOne('JobExec')
    ex_date = Field(DateTime)
    ex_type = Field(Unicode(10))
    ex_comment = Field(UnicodeText)

def init():
    os.remove( datafile )
    setup_all()
    create_all()

def populate():
    ## create d'un agent 
    a1 = Agent(name=u"Agent1")
    a1.description = u"Agent pour test"
    a1.server_name = u"localhost"
    a1.server_ip = u"127.0.0.1"
    a1.server_port = 6000
    session.commit()

def test():
    if os.path.exists( datafile ):
        print "Effacement fichier de test %s " % datafile
        os.remove( datafile )
    setup_all()
    create_all()
    ## Creation d'un agent
    a1 = Agent(name=u"Agent1")
    a1.description = u"Agent pour test"
    a1.server_name = u"localhost"
    a1.server_ip = u"127.0.0.1"
    a1.server_port = 6000

    ## Creons quelques job pour voir
    j1 = Job(name=u"TEST1", cmd = u"ls -l" )
    j1.description = u"test de job pour valider la base de donnees"
    ex1 = JobExec( job = j1 )
    ex1.start_date = datetime.datetime.now()
    ex1.end_date = datetime.datetime.now()
    j1.job_exec.append( ex1 )
    session.commit()
        

if __name__ == '__main__':
    pass
    #test()
