import sqlite3
import UserDict
import job
from sqlalchemy.ext.sqlsoup import SqlSoup
import pdb

##
##
##
class JobManager(dict):
    def __init__(self, dbname=None, *args, **kw):
        self.dbname = dbname
        dict.__init__(self, *args, **kw)

    def initdb(self):
        db = sqlite3.connect(self.dbname)
        c = db.cursor()
        c.execute( """ drop table if exists jobs """ )
        c.execute( """
            create table jobs
                (
                id integer primary key,
                cle varchar(20) unique, 
                job_yaml text
                )
            """)
        c.close()
        db.close()
        
    def load(self):
        db = SqlSoup('sqlite:///%s' % self.dbname)
        for j in db.jobs.all():
            jo = job.Job()
            jo = jo.from_y( j.job_yaml )
            self[j.cle] = jo

    def save(self):
        db = sqlite3.connect(self.dbname)
        c = db.cursor()
        for j in self.keys():
            c.execute(""" 
                insert into jobs values ( NULL, :cle, :job_y )
            """, 
            { 'cle':self[j].name, 'job_y':self[j].to_y() } 
            )
        db.commit()
        c.execute('select * from jobs')
        for row in c:
            print row
        c.close()
        db.close()
        
if __name__ == '__main__':
    jm = JobManager(dbname='dict_jobs.dbf')
    jm.initdb()
    for x in range(1, 20):
        cle = 'J%02d' % x
        jm[cle] = job.Job() 
        jm[cle].name = cle
        jm[cle].cmd = "ls -l"
    jm.save()
    del jm
    pdb.set_trace()
    jm = JobManager(dbname='dict_jobs.dbf')
    jm.load()
    pdb.set_trace()
