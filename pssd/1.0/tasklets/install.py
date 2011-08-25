__author__ = 'aserver'
__tags__   = 'install',

import os

def main(q, i, params, tags):
    qpackage = params['qpackage']
#    setup_path = q.system.fs.joinPaths(qpackage.getPathFiles(), str(q.enumerators.PlatformType.GENERIC), 'swift_security_delegate')
#    egg_path = q.system.fs.joinPaths(os.path.sep, 'usr', 'local', 'lib', 'python2.6', 'dist-packages', 'pssd-1.0-py2.6.egg')
#    q.system.fs.remove(egg_path, onlyIfExists=True)
#    q.system.process.run('python setup.py install', cwd=setup_path)
#    q.system.unix.chown(egg_path, 'root', 'root')
    qpackage.copyFiles()

