
__author__ = 'aserver'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesexportDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version)
    q.system.fs.removeDirTree(qpackage.getPathFiles())

    # source dir
    srcDir = q.system.fs.joinPaths(filesexportDir, 'pscsync')

    # dst dir, and create it
    dstDir = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic/pyapps/pscsync')
    q.system.fs.createDir(dstDir)

    # copy extension files
    q.system.fs.copyDirTree(src = srcDir, dst = dstDir, overwriteDestination = True)
    
