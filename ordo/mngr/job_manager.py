import sqlite3

class JobManager(list):
    def __init__(self, dbname='job.dbf'):
        self.dbname = dbname


if __name__ == '__main__':
    jm = JobManager(dbname="./test.dbf")

