
__author__ = 'aserver'
__tags__   = 'install',

def main(q, i, params, tags):
    #unused = raw_input("install: 1")
    qpackage = params['qpackage']
    #@SEEME: how to check if reinstall?
    q.console.echo("Install %s %s START" % (qpackage.name, qpackage.version))
    checkDir = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic/lib/pylabs/extensions/plist')
    if not q.system.fs.exists(checkDir):
        qpackage.copyFiles()
    else:
        srcDir = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic/lib/pylabs/extensions/plist')
        srcDirDiff = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic/lib/pylabs/extensions/plist/diff')
    
        dstDir = q.system.fs.joinPaths(q.dirs.extensionsDir, 'plist')
        q.system.fs.createDir(dstDir)
        dstDirDiff = q.system.fs.joinPaths(q.dirs.extensionsDir, 'plist/diff')
        q.system.fs.createDir(dstDirDiff)
    
        #unused = raw_input("install: 2")
    
        srcFiles = ['__init__.py', 'Archiver.py', 'enums.py', 'extension.cfg', 'filePatch.py', 'FileProperties.py', 'fsbridge.py', 'PFile.py', 'PFilter.py', 'PFind.py', 'PListFactory.py', 'PList.py']
        for srcFile in srcFiles:
            q.system.fs.copyFile(q.system.fs.joinPaths(srcDir, srcFile), 
                                    q.system.fs.joinPaths(dstDir, srcFile))
        srcFilesDiff = ['__init__.py', 'RSyncLib.py' ]
        for srcFile in srcFilesDiff:
            q.system.fs.copyFile(q.system.fs.joinPaths(srcDirDiff, srcFile), 
                                    q.system.fs.joinPaths(dstDirDiff, srcFile))
    
    q.console.echo("Install %s %s DONE" % (qpackage.name, qpackage.version))
    #unused = raw_input("install: 3")

    #unused = raw_input("install: 4")


