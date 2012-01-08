
import job

## ---------------------------------
## Un dictionnaire avec une liste 
## ---------------------------------
class JobList(dict):
    def add( self, job):
        self[job.name] = job
        print "add %s " % self

    def pr( self, job_name=None ):
        if job_name:
            print self[job_name].pr()
        else:
            for k in self.keys():
                print k, self[k]

if __name__ == '__main__':
    jl = JobList()
    j1 = job.Job()
    j1.name = "J1"
    j1.cmd = "ls -l"
    jl['J1'] = j1
    j3 = job.Job()
    j3.name = "J3"
    j3.cmd = "ls -l"
    jl['J3'] = j3
    print "==============="
    jl.pr()
    print "==============="
    jl.pr('J3')

