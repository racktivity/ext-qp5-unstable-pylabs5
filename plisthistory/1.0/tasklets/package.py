
__author__ = 'aserver'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesexportDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version)
    q.system.fs.removeDirTree(qpackage.getPathFiles())

    # source dir
    srcDir = q.system.fs.joinPaths(filesexportDir, 'synclib/plisthistory')

    # dst dir, and create it
    dstDir = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic/lib/pylabs/extensions/plisthistory')
    q.system.fs.createDir(dstDir)

    # copy extension files
    srcFiles = ['authx.py', 'extension.cfg', '__init__.py', 'PListView.py', 'PListHistory.py', 'plock.py']
    for srcFile in srcFiles:
        q.system.fs.copyFile(q.system.fs.joinPaths(srcDir, srcFile), 
                             q.system.fs.joinPaths(dstDir, srcFile))

    
