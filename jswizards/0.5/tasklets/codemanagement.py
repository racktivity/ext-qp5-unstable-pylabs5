
__author__ = 'incubaid'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    repository = 'https://bitbucket.org/despiegk/jswizards/'
    branch = 'default'

    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()
    connection = i.config.clients.mercurial.findByUrl(repository)

    filesexportDir = q.system.fs.joinPaths(q.dirs.varDir, 'src', qpackage.name, 'files')

    if q.system.fs.exists(filesexportDir):
        q.system.fs.removeDirTree(filesexportDir)

    recipe.addRepository(connection)
    recipe.addSource(connection, '', q.system.fs.joinPaths(filesexportDir, 'www', 'jswizards'), branch=branch)
    recipe.executeTaskletAction(params['action'])

