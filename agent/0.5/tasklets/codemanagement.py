__author__ = 'incubaid'
__tags__     = "codemanagement",
__priority__ = 1

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    qpackage = params['qpackage']
    repository = ['https://bitbucket.org/despiegk/pylabs_agent/']
    branch = ['pylabs5']

    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()
    connection = i.config.clients.mercurial.findByUrl(repository[0])

    filesexportDir = q.system.fs.joinPaths(q.dirs.varDir, 'src', qpackage.name, 'files')

    if q.system.fs.exists(filesexportDir):
        q.system.fs.removeDirTree(filesexportDir)

    recipe.addRepository(connection)
    recipe.addSource(connection, q.system.fs.joinPaths('agent'), q.system.fs.joinPaths(filesexportDir, 'lib', 'pylabs','extensions','agent'), branch=branch[0])
    recipe.addSource(connection, q.system.fs.joinPaths('agent_service'), q.system.fs.joinPaths(filesexportDir, 'apps', 'applicationserver', 'services', 'agent_service'), branch=branch[0])

    q.logger.log("Executing %s action" % params['action'], 1)
    recipe.executeTaskletAction(params['action'])
