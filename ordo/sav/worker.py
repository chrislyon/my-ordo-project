import subprocess
import datetime

## --------------------------------------------------------
## Class de Base pour le job a faire
## Historiquement => on renverse la chaine donnee en entree
## Modification => on execute un job ( shellscript, ...)
## --------------------------------------------------------
class Worker:
    def __init__(self):
        self.history = []
    
    def set_ilog(self, msg):
        ts = datetime.datetime.now().strftime('%d.%m %X')
        return "%s %s" % (ts, msg)

    def work(self, cmd_string):
        
        ilog = []
        ilog.append( self.set_ilog("Debut execution cmd=[%s]" % cmd_string))
        ilog.append( self.set_ilog("Ajout dans l'historique"))
        self.history.append(cmd_string)
        ## execution de la commande
        ilog.append( self.set_ilog("Lancement du jobs"))
        proc = subprocess.Popen(
            cmd_string,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        ## on recupere les infos 
        ilog.append( self.set_ilog("Recuperation des sorties err out"))
        (out, err) = proc.communicate()
        #print "rc     = %s" % proc.returncode
        #print "stderr = %s" % err
        #print "stdout = %s" % out
        ilog.append( self.set_ilog("stderr : %s ligne(s)" % len(err)))
        ilog.append( self.set_ilog("stdout : %s ligne(s)" % len(out)))
        ilog.append( self.set_ilog("Fin execution rc=[%s]" % proc.returncode))
        return (proc.returncode, err, out, cmd_string, ilog)

if __name__ == '__main__':
    w = Worker()
    print "============= ok "
    print w.work("ls -l")
    print "============= ok "
    print w.work("xlxlx")
