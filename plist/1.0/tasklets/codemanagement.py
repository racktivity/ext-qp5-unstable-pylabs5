
__author__ = 'aserver'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params['qpackage']

    #unused = raw_input("codemanagement: 1")
    q.console.echo("Checkout %s %s START" % (qpackage.name, qpackage.version))
    # create temp location
    filesexportDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version)
    q.system.fs.removeDirTree(filesexportDir)

    #print 'codemanagement: filesexportDir=%s' % filesexportDir

    #unused = raw_input("codemanagement: 2")

    # connection
    connection = i.config.clients.mercurial.findByUrl('https://bitbucket.org/Krisdepeuter/private_storage_cloud')

    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()
    recipe.addRepository(connection)
    recipe.addSource(connection, 'synclib/plist', q.system.fs.joinPaths(filesexportDir, 'synclib', 'plist'))

    #unused = raw_input("codemanagement: 3")

    recipe.executeTaskletAction(params['action'])

    q.console.echo("Checkout %s %s DONE" % (qpackage.name, qpackage.version))
    #unused = raw_input("codemanagement: 4")

