__author__ = 'incubaid'
__tags__     = "codemanagement",
__priority__ = 1

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    qpackage = params['qpackage']
    repository = ['http://bitbucket.org/despiegk/osis']
    branch = ['0.5']

    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()
    connection = i.config.clients.mercurial.findByUrl(repository[0])
    recipe.addRepository(connection)
    recipe.addSource(connection, q.system.fs.joinPaths('code','osis'), q.system.fs.joinPaths('var', 'src', 'lib', 'python', 'site-packages','osis'),branch=branch[0])
    recipe.addSource(connection, q.system.fs.joinPaths('osis_connection_config'), q.system.fs.joinPaths('var', 'src', 'lib', 'pymonkey', 'extensions', 'osis_connection'),branch=branch[0])

    if params['action'] == 'getSource':
        params['action'] = 'export'

    q.logger.log("Executing %s action" % params['action'], 1)
    recipe.executeTaskletAction(params['action'])
