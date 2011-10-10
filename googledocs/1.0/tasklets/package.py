
__author__ = 'aserver'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesexportDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version)
    q.system.fs.removeDirTree(qpackage.getPathFiles())

    # source dir
    srcDir = q.system.fs.joinPaths(filesexportDir, 'synclib/googledocs')

    # dst dir, and create it
    dstDir = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic/lib/pylabs/extensions/googledocs')
    q.system.fs.createDir(dstDir)

    # copy extension files
    srcFiles = ['__init__.py', 'gd.py', 'GDocsSync.py', 'GDocsSyncFactory.py', 'extension.cfg']
    for srcFile in srcFiles:
        q.system.fs.copyFile(q.system.fs.joinPaths(srcDir, srcFile), 
                             q.system.fs.joinPaths(dstDir, srcFile))

    
