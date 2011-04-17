__author__ = 'incubaid'
__tags__   = 'install',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    for copyme in ("apps", "libexec", 'www'):
        q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackage.getPathFiles(), "generic", copyme), q.system.fs.joinPaths(q.dirs.baseDir, copyme))
    qpackage.signalConfigurationNeeded()