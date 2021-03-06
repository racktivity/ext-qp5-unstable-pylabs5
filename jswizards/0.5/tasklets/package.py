
__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesDir = qpackage.getPathFiles()
    q.system.fs.removeDirTree(filesDir)
    q.system.fs.createDir(filesDir)
    q.system.fs.copyDirTree(qpackage.getPathSourceCode(), qpackage.getPathFiles())
    
    filesexportDir = q.system.fs.joinPaths(filesDir, str(q.enumerators.PlatformType.GENERIC))    
    coffeePath = q.system.fs.joinPaths(filesexportDir, 'www', 'jswizards', 'js', 'jswizards.coffee')
    q.system.fs.removeFile(coffeePath)
    
    hgdirPath = q.system.fs.joinPaths(filesexportDir, 'www', 'jswizards', '.hg')
    q.system.fs.removeDirTree(hgdirPath)
