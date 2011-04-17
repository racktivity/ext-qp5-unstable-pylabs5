__author__ = 'incubaid'
__tags__     = "codemanagement",
__priority__ = 1

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    qpackage = params['qpackage']
    repository = ['http://bitbucket.org/despiegk/pylabs_workflowengine']
    branch = ['pylabs5']

    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()
    connection = i.config.clients.mercurial.findByUrl(repository[0])
    recipe.addRepository(connection)
    recipe.addSource(connection, q.system.fs.joinPaths('workflowengine','lib'), q.system.fs.joinPaths('var', 'src', 'lib', 'python','site-packages','workflowengine'), branch=branch[0])
    recipe.addSource(connection, q.system.fs.joinPaths('workflowengine','manage'), q.system.fs.joinPaths('var', 'src', 'lib', 'pylabs','extensions','workflowengine','manage'), branch=branch[0])
    recipe.addSource(connection, q.system.fs.joinPaths('workflowengine','bin'), q.system.fs.joinPaths('var', 'src', 'apps', 'workflowengine', 'bin'), branch=branch[0])
    recipe.addSource(connection, q.system.fs.joinPaths('workflowengine','debug_service'), q.system.fs.joinPaths('var', 'src', 'apps', 'applicationserver', 'services', 'wfe_debug'), branch=branch[0])

    if params['action'] == 'getSource':
        params['action'] = 'export'

    q.logger.log("Executing %s action" % params['action'], 1)
    recipe.executeTaskletAction(params['action'])
