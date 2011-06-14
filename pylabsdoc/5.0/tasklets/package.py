
__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesDir = qpackage.getPathFiles()
    q.system.fs.removeDirTree(filesDir)
    q.system.fs.createDir(filesDir)
    relativePath = q.system.fs.joinPaths("generic", "pyapps", "pylabsdoc")
    sourcePath = q.system.fs.joinPaths(q.system.fs.joinPaths(qpackage.getPathSourceCode(), relativePath))
    q.system.fs.copyDirTree(sourcePath, q.system.fs.joinPaths(filesDir, relativePath))

