__author__ = 'aserver'
__tags__   = 'install',

import os

def main(q, i, params, tags):
    qpackage = params['qpackage']
    qpackage.copyFiles()
    setup_path = q.system.fs.joinPaths(q.dirs.tmpDir, 'swift_security_delegate')
    egg_path = q.system.fs.joinPaths(os.path.sep, 'usr', 'local', 'lib', 'python2.6', 'dist-packages', 'pssd-%s-py2.6.egg' % qpackage.version)
    q.system.fs.remove(egg_path, onlyIfExists=True)
    q.system.process.run('python setup.py install', cwd=setup_path)
    q.system.unix.chown(egg_path, 'root', 'root')
    # We don't need setup path anymore
    q.system.fs.removeDirTree(setup_path)

