
__author__ = 'aserver'
__tags__   = 'install',

def main(q, i, params, tags):
    qpackage = params['qpackage']

    # download the util/env_setup/initial_config.sh and cgi-bin/file_receiver.cgi files 
    # into a temporary location

    # prepare destination directory
    q.console.echo('Prepare destination directory...')
    dstDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version)
    q.console.echo('  Destination directory is "%s".' % dstDir)
    q.console.echo('Cleanup destination directory "%s"...' % dstDir)
    q.system.fs.removeDirTree(dstDir)
    q.console.echo('  Destination directory "%s" cleaned up.' % dstDir)

    # get the files into dstDir
    q.console.echo('Getting files from repository...')
    connection = i.config.clients.mercurial.findByUrl('https://bitbucket.org/Krisdepeuter/private_storage_cloud')
    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()
    recipe.addRepository(connection)
    recipe.addSource(connection, 'util/env_setup', q.system.fs.joinPaths(dstDir, 'util', 'env_setup'))
    recipe.addSource(connection, 'cgi-bin', q.system.fs.joinPaths(dstDir, 'cgi-bin'))
    recipe.executeTaskletAction('checkout')
    # remove the package files and let just the two files mentioned above
    pakDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version, 'util', 'env_setup', 'packages')   
    q.console.echo('Removing unnecessary files from destination directory "%s"...' % pakDir)
    q.system.fs.removeDirTree(pakDir)
    q.console.echo('  Directory "%s" removed.' % pakDir)

    """
        ok, now we have in /opt/qbase/var/tmp/pscsync_interfaces/1.0:
            /cgi-bin
              file_receiver.cgi
            /util
              /env_setup
                initial_config.sh
    """
    # prepare environment
    q.console.echo('Preparing environment for executing configure script.')
    curDir = q.system.fs.getcwd()
    q.console.echo('  Current directory is "%s".' % curDir)
    scriptPath = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version, 'util', 'env_setup')
    q.console.echo('  Changing current directory to script directory "%s".' % scriptPath)
    q.system.fs.changeDir(scriptPath)
    q.console.echo('  Current directory was changed to "%s".' % q.system.fs.getcwd())
    # executing script
    q.console.echo('Executing initial_config.sh')
    q.system.process.executeInSandbox('./initial_config.sh')
    # restore environment
    q.console.echo('Restoring environment.')
    q.console.echo('  Current directory is "%s".' % q.system.fs.getcwd())
    q.console.echo('  Restoring directory to "%s".' % curDir)
    q.system.fs.changeDir(curDir)
    q.console.echo('  Current directory is now "%s".' % curDir)

    # done
    q.console.echo('%s v%s - Installation finished.' % (qpackage.name, qpackage.version))

