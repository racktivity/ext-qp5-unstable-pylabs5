
__author__ = 'aserver'
__tags__   = 'install',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    setup_path = q.system.fs.joinPaths(qpackage.getPathSourceCode(), str(q.enumerators.PlatFormType.GENERIC), 'swift_security_delegate')
    q.system.process.run('python setup.py install', cwd=setup_path)

