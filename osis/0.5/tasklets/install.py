import sys

__author__ = 'incubaid'
__tags__ = 'install',
__priority__ = 1

def match(q, i, params, tags):
    return True
    
def main(q, i, params, tags):
    
    qpackage = params['qpackage']
    
    pyversion = q.qpackagetools.getPythonVersion() 
    
    src_egg = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic', 'osis_egg',  qpackage.name + '.egg.zip')
    target_egg_name = qpackage.name + '-' + qpackage.version +'-py' + pyversion  + '.egg'
    target_egg = q.system.fs.joinPaths(q.dirs.baseDir, 'lib', 'python', 'site-packages', target_egg_name)

    q.qpackagetools.copyEggToSandbox(src_egg, target_egg)

    q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic', 'lib'), q.system.fs.joinPaths(q.dirs.baseDir, 'lib'))
