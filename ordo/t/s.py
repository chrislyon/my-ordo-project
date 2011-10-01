import datetime, time
import sched

def my_event(msg=None):
    t = datetime.datetime.now()
    if not msg:
        print "Event : ", t.strftime("%x %X %f")
    else:
        print "%s" % msg, t.strftime("%x %X %f")


def do_it():
    my_event("Lancement du scheduler")
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1000,1000,my_event("JOB1"), ())
    #s.enter(10,1,my_event("JOB2"), ())
    print s.queue
    s.run()
    my_event("Fin du scheduler")

if __name__ == "__main__":
    do_it()
