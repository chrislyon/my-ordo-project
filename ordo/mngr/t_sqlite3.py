import sqlite3

#db = sqlite3.connect(":memory:")
db = sqlite3.connect("jobs.dbf")

c = db.cursor()

try:
    c.execute(""" select count(*) from jobs """)
except:
    c.execute(""" create table jobs ( id integer primary key, job_name varchar(10), job_cmd text ) """)

c.execute(""" insert into jobs values(NULL, 'TEST1', 'ls -l') """)
c.execute(""" insert into jobs values(NULL, 'TEST2', 'ls -l') """)
c.execute(""" insert into jobs values(NULL, 'TEST3', 'ls -l') """)
c.execute(""" insert into jobs values(NULL, 'TEST4', 'ls -l') """)

db.commit()

c.close()
db.close()
