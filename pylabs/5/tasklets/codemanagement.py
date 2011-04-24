__author__ = 'incubaid'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params['qpackage']

    repository = 'https://bitbucket.org/incubaid/pylabs-core/'
    branch = 'default'

    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()
    connection = i.config.clients.mercurial.findByUrl(repository)

    filesexportDir = q.system.fs.joinPaths(q.dirs.varDir, 'src', qpackage.name, 'files')

    if q.system.fs.exists(filesexportDir):
        q.system.fs.removeDirTree(filesexportDir)

    recipe.addRepository(connection)
    recipe.addSource(connection, q.system.fs.joinPaths('qbase5'), q.system.fs.joinPaths(filesexportDir), branch=branch)
    recipe.addSource(connection, q.system.fs.joinPaths('apps', 'applicationserver'), q.system.fs.joinPaths(filesexportDir, 'apps', 'applicationserver'), branch=branch)
    recipe.addSource(connection, q.system.fs.joinPaths('apps', 'cloud_api_generator'), q.system.fs.joinPaths(filesexportDir, 'apps', 'cloud_api_generator'), branch=branch)
    recipe.addSource(connection, q.system.fs.joinPaths('core'), q.system.fs.joinPaths(filesexportDir, 'lib', 'pylabs', 'core', 'pylabs'), branch=branch)
    recipe.addSource(connection, q.system.fs.joinPaths('extensions'), q.system.fs.joinPaths(filesexportDir, 'lib', 'pylabs', 'extensions'), branch=branch)
    recipe.addSource(connection, q.system.fs.joinPaths('lib'), q.system.fs.joinPaths(filesexportDir, 'lib', 'python', 'site-packages'), branch=branch)
    recipe.addSource(connection, q.system.fs.joinPaths('utils'), q.system.fs.joinPaths(filesexportDir, 'utils'), branch=branch)
    recipe.executeTaskletAction(params['action'])
    q.system.fs.removeDirTree(q.system.fs.joinPaths(filesexportDir, 'cfg', 'qpackages4'))
