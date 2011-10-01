#!  /usr/bin/python
# -*- coding: UTF8 -*-
##----------------------------------------------------
## Projet        :  ordo
## Version       :  Alpha 0.0
## Auteur        :  chris
## Date Creation :  13/09/2011 11:36:15
## Objet         : agent.py
## MAJ           : 
## Bug Report    : 
## Todo List     : 
##----------------------------------------------------
## $Id :$
##----------------------------------------------------
## (c)  chris 2011
##----------------------------------------------------

## ---------------------------------------------
## Origine multiservice.py => Twisted Book
##
## Modifie par chris Sept 2011
##
## ---------------------------------------------
"""
"""

from twisted.application import service, internet
from twisted.application.internet import TCPServer
from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic
from twisted.web import resource, server as webserver

from twisted.application.service import Application

from twisted.spread import pb

from  worker import Worker
from job import Job

## -------------------------------
## Le protocole telnet de base
## -------------------------------
class WorkerLineProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        if hasattr(self, 'handle_' + line):
            getattr(self, 'handle_' + line)()
        else:
            ## ce n'est une fonction interne 
            ## donc c'est une commande a passer
            ## on doit creer un job 
            j = Job()
            j.name = "JOB 0001"
            j.cmd = line
            self.factory.worker.job = j
            self.factory.worker.work()
            #rc, err, out, cmd, ilog = self.factory.worker.work()
            self.sendLine( "Commande : %s " % j.cmd )
            self.sendLine( "Return Code = %s " % j.returncode )
            if j.stderr:
                self.sendLine( "Err = %s" % j.stderr )
            if j.stdout:
                self.sendLine( "Out = %s" % j.stdout )

            for l in j.ilog:
                self.sendLine( "> %s " % l )

    ## si je tape help => alors
    def handle_help(self):
        self.sendLine("Help bientot dispo ...")

    ## si je tape quit => alors 
    def handle_quit(self):
        self.transport.loseConnection()

## ------------------------------------
## La fabrique pour l'acces telnet
## ------------------------------------
class WorkerLineFactory(protocol.ServerFactory):
    protocol = WorkerLineProtocol
    
    def __init__(self, worker):
        self.worker = worker

## -------------------------------
## En cas d'acces via le web
## -------------------------------
class WorkerPage(resource.Resource):
    def __init__(self, worker):
        self.worker = worker
        
    def render(self, request):
        if request.args.has_key("string"):
            string = request.args["string"][0]
            j = Job()
            j.name = "JOB 0001"
            j.cmd = string
            self.worker.job = j
            self.worker.work()
            #rc, err, out, cmd, ilog  = self.worker.work(string)
            rc = j.returncode
            err = j.stderr
            out = j.stdout
            cmd = j.cmd
            ilog = j.ilog
        else:
            rc, err, out, cmd, ilog  = ( 0, "", "", "<>", [] )

        rep = """
        <html><body><form>
        <input type='text' name='string' value='%s' />
        <input type='submit' value='Go' />
        """
        rep += "<hr/>"
        rep += "<table border=1>"
        rep += "<tr>"
        rep += "<th> Libelle </th>"
        rep += "<th> Valeur  </th>"
        rep += "</tr>"

        rep += "<tr>"
        rep += "<td> Commande  </td>"
        rep += "<td>  %s </td>" % cmd
        rep += "</tr>"

        rep += "<tr>"
        rep += "<td> stderr </td>"
        rep += "<td>  %s </td>" % err
        rep += "</tr>"

        rep += "<tr>"
        rep += "<td> stdout </td>"
        rep += "<td>  %s </td>" % out
        rep += "</tr>"

        for l in ilog:
            rep += "<tr>"
            rep += "<td></td>"
            rep += "<td> %s </td>" % l
            rep += "</tr>"

        rep += "</table>"
        rep +=  """
        </form></body></html>
        """
               
        return rep

## --------------------------
## Acces Perspective Broker
## Permet des remote function
## pas de factory elle est generique
## --------------------------
class PbWorker(pb.Root):
    def __init__(self):
        self.worker = Worker()

    #def remote_echo(self, st):
    #    print 'receiving string :', st
    #    return st

    def remote_work(self, js):
        self.worker.job = Job()
        self.worker.job.from_y(js)
        j = self.worker.job
        print 'receiving job :', j
        print "job.name = %s " % j.name
        print "job.cmd = %s " % j.cmd
        self.worker.work()
        return self.worker.job.to_y()

## -----------------------------------------------
## Acces Admin qui stop ou demarre les services
## -----------------------------------------------
class ServiceAdminPage(resource.Resource):
    def __init__(self, app):
        self.app = app

    def render_GET(self, request):
        request.write("""
        <html><body>
        <h1>Current Services</h1>
        <form method='post'>
        <ul>
        """)
        for srv in service.IServiceCollection(self.app):
            if srv.running:
                checked = "checked='checked'"
            else:
                checked = ""
            request.write("""
            <input type='checkbox' %s name='service' value='%s'>%s<br />
            """ % (checked, srv.name, srv.name))
        request.write("""
        <input type='submit' value='Go' />
        </form>
        </body></html>
        """)
        return ''

    def render_POST(self, request):
        actions = []
        serviceList = request.args.get('service', [])
        for srv in service.IServiceCollection(self.app):
            if srv.running and not srv.name in serviceList:
                stopping = defer.maybeDeferred(srv.stopService)
                actions.append(stopping)
            elif not srv.running and srv.name in serviceList:
                # wouldn't work if this program were using reserved ports
                # and running under an unprivileged user id
                starting = defer.maybeDeferred(srv.startService)
                actions.append(starting)
        defer.DeferredList(actions).addCallback( self._finishedActions, request)
        return webserver.NOT_DONE_YET

    def _finishedActions(self, results, request):
        request.redirect('/')
        request.finish()

## --------------------------------------------
## La partie principale
## => doit être lance par twistd -y $0.py
## --------------------------------------------

## ----------------------------
## L'application principale
## ----------------------------
application = service.Application("AGENT")
## l'objet de base que l'on partage
worker = Worker()

lineService = internet.TCPServer(2323, WorkerLineFactory(worker))
lineService.setName("Telnet")
lineService.setServiceParent(application)

## -------------
## L'acces web
## -------------
webRoot = resource.Resource()
webRoot.putChild('', WorkerPage(worker))
webService = internet.TCPServer(8000, webserver.Site(webRoot))
webService.setName("Web")
webService.setServiceParent(application)

## ----------------
## L'acces admin
## ----------------
webAdminRoot = resource.Resource()
webAdminRoot.putChild('', ServiceAdminPage(application))
webAdminService = internet.TCPServer(8001, webserver.Site(webAdminRoot))
webAdminService.setName("WebAdmin")
webAdminService.setServiceParent(application)

## --------------------------
## Acces Perspective Broker
## --------------------------
serverfactory = pb.PBServerFactory(PbWorker())
PbServerService = TCPServer(8789, serverfactory)
PbServerService.setServiceParent(application)

