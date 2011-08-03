__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesDir = qpackage.getPathFiles()
    q.system.fs.removeDirTree(filesDir)
    q.system.fs.createDir(filesDir)
    q.system.fs.copyDirTree(qpackage.getPathSourceCode(), qpackage.getPathFiles())

