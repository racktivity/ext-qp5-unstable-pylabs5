__author__ = 'incubaid'
__tags__   = 'install',

def main(q, i, params, tags):
    import os
    qpackage = params['qpackage']
    debfile = os.path.join(qpackage.getPathFiles(), 'linux64', 'arakoon_tip_amd64.deb' )
    q.platform.ubuntu.installDebFile(debfile)
