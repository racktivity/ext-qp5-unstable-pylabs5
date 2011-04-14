__author__ = 'incubaid'
__tags__   = 'codemanagement',

def main(q, i, params, tags):

    package = params['qpackage']
    
    # Package info
    name       = package.name
    version    = package.version
    
    # Repo info
    repository = 'https://bitbucket.org/despiegk/pymodel'
    branch     = 'default' # 'v%s' % version
    
    # Map repo to sandbox
    paths = (
        (q.system.fs.joinPaths('', 'pymodel'), q.system.fs.joinPaths('', 'lib', 'python', 'site-packages', 'pymodel')), 
        (q.system.fs.joinPaths('', 'pymodel_extension'), q.system.fs.joinPaths('', 'lib', 'pymonkey', 'extensions', 'pymodel_extension')),
    )

    # Setup recipe
    from clients.mercurial.HgRecipe import HgRecipe
    connection = i.config.clients.mercurial.findByUrl(repository)
    recipe = HgRecipe()
    recipe.addRepository(connection)
    
    for source, destination in paths:
        recipe.addSource(connection, source, q.system.fs.joinPaths(package.getPathSourceCode(),'generic' , destination), branch=branch)
        
    # Execute the action
    recipe.executeTaskletAction(params['action'])
