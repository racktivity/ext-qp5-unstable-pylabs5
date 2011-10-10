
__author__ = 'aserver'
__tags__   = 'install',

def main(q, i, params, tags):
    # download the gdata 2.0.14 package, and extract it PyLabs temporary directory

    #
    # step 1: download gdata 2.0.14 and uncompress on pylabs' tmp
    #
    downloadSource = 'http://gdata-python-client.googlecode.com/files/'
    packageName = 'gdata-2.0.14'
    fileName = '%s.tar.gz' % (packageName)

    # remote file
    #print 'downloading remote archive'
    remoteArchive = q.system.fs.joinPaths(downloadSource, fileName)
    #print 'remoteArchive=%s' % remoteArchive

    # local file
    localArchive = 'file://%s' % q.system.fs.joinPaths(q.dirs.tmpDir, fileName)
    #print 'localArchive=%s' % localArchive

    # copy remote to local
    #print 'copying %s to %s' % (remoteArchive, localArchive)
    q.cloud.system.fs.copyFile(remoteArchive, localArchive)

    # uncompress local
    sourceFile = q.system.fs.joinPaths(q.dirs.tmpDir, fileName)
    destinationDir = q.system.fs.joinPaths(q.dirs.tmpDir)
    #print 'uncompressing %s to %s' % (sourceFile, destinationDir)
    q.system.fs.targzUncompress(sourceFile, destinationDir, False)

    #
    # step 2: perform gdata install
    #
    #print 'composing setup'
    import os
    curDir = os.getcwd()
    #print 'current directory is: %s' % os.getcwd()

    setupDir = q.system.fs.joinPaths(destinationDir, packageName)
    os.chdir(setupDir)
    #print 'current directory is now to: %s' % os.getcwd()

    import subprocess
    setupCommand = 'python setup.py install' 
    result = subprocess.Popen('%s' % setupCommand, shell=True, stdout = subprocess.PIPE).communicate()[0]
    #print result

    # restore directory
    os.chdir(curDir)
    #print 'current directory is back to: %s' % os.getcwd()

    # check installation
    #print 'checking gdata installation...'
    try:
        import gdata
        print 'gdata import OK, installation successful'
    except Exception, ex:
        print 'gdata import failed, installation failed'

    print 'install END'
    return 

