__author__ = 'incubaid'
__tags__ = 'backup',

def main(q, i, params, tags):
    qpackage = params['qpackage']

    backupurl=params['backupurl'] #e.g. ftp://login:passwd@10.10.1.1/myroot/ @point to doc about cloudfilesystem
    if params['action']=="backup":
        pass

    if params['action']=="restore":
        pass

    if params['action']=="backupconfig":
        pass

    if params['action']=="restoreconfig":
        pass
