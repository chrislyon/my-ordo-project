
import job

class JobList(dict):
    def add( self, job ):
        self[job.name] = job

    def pr( self, job_name=None ):
        if job_name:
            print job_name, self[job_name]
        else:
            for k in self.keys():
                print k, self[k]

if __name__ == '__main__':
    jl = JobList()
    j1 = job.Job()
    j1.name = "J1"
    j1.cmd = "ls -l"
    jl.add( j1 )
    jl.pr()

