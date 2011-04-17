__author__ = "incubaid"
__tags__     = "install",
__priority__ = 1

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    # Copy the files for this platform from the files/ folder to sandbox
    qpackage = params['qpackage']
    py2_6 = q.system.fs.joinPaths(q.dirs.baseDir, 'lib', 'python2.6', 'site-packages', 'workflowengine')
    if q.system.fs.exists(py2_6): q.system.fs.removeDirTree(py2_6)

    qpackage.copyFiles()
    qpackage.signalConfigurationNeeded()
