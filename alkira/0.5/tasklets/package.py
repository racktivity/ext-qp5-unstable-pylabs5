__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesexportDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version )
    q.system.fs.removeDirTree(qpackage.getPathFiles())
    q.system.fs.copyDirTree(filesexportDir, q.system.fs.joinPaths(qpackage.getPathFiles(), "generic"))