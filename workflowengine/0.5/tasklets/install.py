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
    q.extensions.enable('q.manage.workflowengine')
    q.extensions.enable('q.workflowengine.agentcontroller')
    q.extensions.enable('q.workflowengine.actionmanager')
    q.extensions.enable('i.config.workflowengine')
    q.extensions.enable('q.workflowengine.jobmanager')

