
__author__ = 'aserver'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    qpfolder = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic'))
    q.system.fs.removeDirTree(qpfolder)
    filesexportDir = q.system.fs.joinPaths(q.dirs.varDir, 'src', qpackage.name, 'files')

    q.system.fs.copyDirTree(filesexportDir, qpfolder)
