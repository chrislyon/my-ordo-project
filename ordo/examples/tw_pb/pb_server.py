from twisted.spread import pb
from twisted.internet import reactor

class Echoer(pb.Root):
    def remote_echo(self, st):
        print 'echoing:', st
        return st

if __name__ == '__main__':
    serverfactory = pb.PBServerFactory(Echoer())
    reactor.listenTCP(8789, serverfactory)
    reactor.run()
