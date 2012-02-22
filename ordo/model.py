## ------------------------------
## Init de la base de donnees
## ------------------------------

import os
import datetime
import elixir
from elixir import *

metadata = elixir.metadata

class Agent(Entity):
    using_options(tablename='AGENT')
    name = Field(Unicode(30))
    description = Field(UnicodeText)
    server_ip = Field(Unicode(30))
    server_name = Field(Unicode(30))
    server_port = Field(Integer)
    password = Field(String(20))
    default_agent = Field(Boolean)

    def liste(self):
        return []

    def __repr__(self):
        return "<Agent : %s>" % self.name

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

def populate():
    ## create d'un agent 
    a1 = Agent(name=u"Agent1")
    a1.description = u"Agent pour test"
    a1.server_name = u"localhost"
    a1.server_ip = u"127.0.0.1"
    a1.server_port = 6000
    a1.default_agent = True
    a1.password = "SECRET"
    session.commit()

def init_from_scratch():
    datafile = "db/data_ordo.sqlite"
    if os.path.exists( datafile ):
        print "Effacement fichier de test %s " % datafile
        os.remove( datafile )
    metadata.bind = "sqlite:///"+datafile

    metadata.bind.echo = True
    metadata.bind.echo = False
    setup_all()
    create_all()
    populate()

def test():
    metadata.bind =  "sqlite:///db/data_ordo.sqlite"
    setup_all()
    a =  Agent.query.first()
    print a.name, a.description
        

if __name__ == '__main__':
    #init_from_scratch()
    test()
    pass
