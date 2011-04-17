__author__ = 'incubaid'
__tags__     = 'install',
__priority__ = 1

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    # Copy the files for this platform from the files/ folder to sandbox
    qpackage = params['qpackage']
    qpackage.copyFiles()
    qpackage.signalConfigurationNeeded()
