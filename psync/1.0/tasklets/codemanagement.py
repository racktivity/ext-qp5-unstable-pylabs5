
__author__ = 'aserver'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params['qpackage']

    # create temp location
    filesexportDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version)
    q.system.fs.removeDirTree(filesexportDir)

    # connection
    connection = i.config.clients.mercurial.findByUrl('https://bitbucket.org/Krisdepeuter/private_storage_cloud')

    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()
    recipe.addRepository(connection)
    recipe.addSource(connection, 'synclib/psync', q.system.fs.joinPaths(filesexportDir, 'synclib', 'psync'))

    recipe.executeTaskletAction(params['action'])

