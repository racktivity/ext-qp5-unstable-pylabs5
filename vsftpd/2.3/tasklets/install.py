__author__ = 'incubaid'
__tags__   = 'install',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    q.platform.ubuntu.install(qpackage.name)
