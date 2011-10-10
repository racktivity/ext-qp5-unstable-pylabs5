
__author__ = 'aserver'
__tags__ = 'package',

def main(q, i, params, tags):
    # pick files from pylabs qpackage directories and copy them to the proper place in the Pylabs sandbox
    #unused = raw_input("package: 1")    
    qpackage = params["qpackage"]
    q.console.echo("Packaging %s %s START" % (qpackage.name, qpackage.version))
    filesexportDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version)
    q.system.fs.removeDirTree(qpackage.getPathFiles())

    #unused = raw_input("package: 2")

    # source directories
    srcDir = q.system.fs.joinPaths(filesexportDir, 'synclib/plist')
    srcDirDiff = q.system.fs.joinPaths(filesexportDir, 'synclib/plist/diff')

    # dst directories, and create them 
    dstDir = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic/lib/pylabs/extensions/plist')
    q.system.fs.createDir(dstDir)
    dstDirDiff = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic/lib/pylabs/extensions/plist/diff')
    q.system.fs.createDir(dstDirDiff)

    #unused = raw_input("package: 3")

    # copy extension files
    srcFiles = ['__init__.py', 'Archiver.py', 'enums.py', 'extension.cfg', 'filePatch.py', 'FileProperties.py', 'PFile.py', 'PFilter.py', 'PFind.py', 'PListFactory.py', 'PList.py', 'fsbridge.py']
    for srcFile in srcFiles:
        q.system.fs.copyFile(q.system.fs.joinPaths(srcDir, srcFile), 
                             q.system.fs.joinPaths(dstDir, srcFile))

    srcFilesDiff = ['__init__.py', 'RSyncLib.py' ]
    for srcFile in srcFilesDiff:
        q.system.fs.copyFile(q.system.fs.joinPaths(srcDirDiff, srcFile), 
                             q.system.fs.joinPaths(dstDirDiff, srcFile))
    
    q.console.echo("Packaging %s %s DONE" % (qpackage.name, qpackage.version))

    #unused = raw_input("package: 4")

    
