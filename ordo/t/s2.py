from datetime import datetime
import time

from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler()
sched.start()

def j1():
    job_function("JOB1")

def j2():
    job_function("JOB2")

def j3():
    job_function("JOB3")

def job_function(msg=None):
    t = datetime.now()
    if not msg:
        print "Event : ", t.strftime("%x %X %f")
    else:
        print "%s" % msg, t.strftime("%x %X %f")

# Schedule job_function to be called every two hours
sched.add_interval_job(j1, minutes=1)

# The same as before, but start after a certain time point
#sched.add_interval_job(j2, start_date='2011-09-27 14:00')

sched.add_cron_job(j3, year='*', month='*', day='*', hour='*', minute='*' )
sched.add_cron_job(j2, year='*', month='*', day='*', hour='*', minute='*', second="10,20,30,40" )

while True:
    time.sleep(20)
    job_function("Liste des jobs : ")
    sched.print_jobs()
