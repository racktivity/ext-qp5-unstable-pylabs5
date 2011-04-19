
__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesDir = q.system.fs.joinPaths(qpackage.getPathFiles())
    q.system.fs.removeDirTree(filesDir)
    q.system.fs.createDir(filesDir)
    filesexportDir = q.system.fs.joinPaths(q.dirs.varDir, 'src', qpackage.name, 'files')    
   
    relativePath = q.system.fs.joinPaths('pyapps', 'sampleapp')
    q.system.fs.copyDirTree(q.system.fs.joinPaths(filesexportDir, relativePath), q.system.fs.joinPaths(filesDir, "generic", relativePath))

