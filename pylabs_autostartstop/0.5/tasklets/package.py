
__author__ = 'aserver'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    metadataDir = qpackage.getPathMetadata()
    filesDir = q.system.fs.joinPaths(qpackage.getPathFiles())

    if q.system.fs.exists(filesDir):
        q.system.fs.removeDirTree(filesDir)

    q.system.fs.createDir(filesDir)

    q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackage.getPathSourceCode(), str(q.enumerators.PlatformType.UNIX), 'files'),
                            q.system.fs.joinPaths(filesDir, 'linux', 'lib', 'pylabs', 'extensions', 'autostart'))

    q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackage.getPathSourceCode(), str(q.enumerators.PlatformType.UNIX), 'tasklets'),
                            q.system.fs.joinPaths(metadataDir, 'tasklets'))

