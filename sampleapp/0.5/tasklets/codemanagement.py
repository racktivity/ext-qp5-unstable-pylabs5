
__author__ = 'aserver'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    #Use this to checkout from mercurial
    #from pylabs.clients.hg.HgRecipe import HgRecipe
    #recipe = HgRecipe()
    
    # Or just extract the files from the bundle
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
    recipe.addSource(connection, q.system.fs.joinPaths('pyapps', 'sampleapp'), q.system.fs.joinPaths(filesexportDir, 'pyapps', 'sampleapp'), branch=branch)

    connection =  i.config.clients.mercurial.findByUrl("http://bitbucket.org/despiegk/lfw")
    recipe.addRepository(connection)
    recipe.addSource(connection, q.system.fs.joinPaths('docs', 'alkiradocs'), q.system.fs.joinPaths(filesexportDir, 'pyapps', 'sampleapp', 'portal', 'spaces', 'alkiradocs'))
    recipe.addSource(connection, q.system.fs.joinPaths('htdocs', 'js', 'macros'), q.system.fs.joinPaths(filesexportDir, 'pyapps', 'sampleapp', 'impl', 'portal', 'jsmacros'))
    recipe.addSource(connection, q.system.fs.joinPaths('docs', 'md_images'), q.system.fs.joinPaths(filesexportDir, 'pyapps', 'sampleapp', 'portal', 'static', 'images', 'alkira'))
    recipe.addSource(connection, 'pylabsmacro', q.system.fs.joinPaths(filesexportDir, 'pyapps', 'sampleapp', 'impl', 'portal', 'pylabsmacro'))

    recipe.executeTaskletAction(params['action'])

