
__author__ = 'aserver'
__tags__   = 'install',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    qpackage.copyFiles()
    #q.platform.ubuntu.check()
    #from pylabs.Shell import *
    #ipshell()
    #q.platform.ubuntu.updatePackageMetadata()
    #q.platform.ubuntu.checkInstall("eric","eric")
    #q.platform.ubuntu.install("python-qt4-sql")
    #path=qpackage.getPathFiles()
    #path=q.system.fs.joinPaths(path,"rootfs")
    #q.system.fs.copyDirTree(path, "/")

