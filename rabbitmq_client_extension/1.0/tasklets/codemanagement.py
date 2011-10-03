
__author__ = 'aserver'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()
    connection = i.config.clients.mercurial.findByUrl('http://bitbucket.org/incubaid/rabbitmq_extension')
    recipe.addRepository(connection)

    qpackage = params['qpackage']
    exportdir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version)
    q.system.fs.removeDirTree(exportdir)

    recipe.addSource(connection, 'rabbitmq_client/', q.system.fs.joinPaths(exportdir, 'lib', 'pylabs', 'extensions', 'baseworking', 'rabbitmq'))
    recipe.addSource(connection, 'rabbitmq_config/', q.system.fs.joinPaths(exportdir, 'lib', 'pylabs', 'extensions', 'interactive', 'rabbitmq'))
    recipe.executeTaskletAction(params['action'])
