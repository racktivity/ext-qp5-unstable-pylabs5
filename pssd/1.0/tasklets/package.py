
__author__ = 'aserver'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    files_path = qpackage.getPathFiles()
    q.system.fs.removeDirTree(files_path)
    q.system.fs.createDir(files_path)
    q.system.fs.copyDirTree(qpackage.getPathSourceCode(), files_path)

