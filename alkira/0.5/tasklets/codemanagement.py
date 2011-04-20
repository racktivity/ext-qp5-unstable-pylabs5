__author__ = 'incubaid'
__tags__ = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesexportDir = q.system.fs.joinPaths(q.dirs.tmpDir, qpackage.name, qpackage.version )
    q.system.fs.removeDirTree(filesexportDir)
    osisdir = q.system.fs.joinPaths(filesexportDir, 'libexec', 'osis')

    from clients.mercurial.HgRecipe import HgRecipe
    recipe = HgRecipe()

    connection =  i.config.clients.mercurial.findByUrl("http://bitbucket.org/despiegk/lfw")
    recipe.addRepository(connection)
    recipe.addSource(connection, 'model/rootobjects/', osisdir)

    q.system.fs.createDir(osisdir)

    recipe.addSource(connection, 'model/views/', q.system.fs.joinPaths(filesexportDir, 'views'))
    recipe.addSource(connection, 'htdocs/', q.system.fs.joinPaths(filesexportDir, 'www', 'lfw'))
    recipe.addSource(connection, 'services/lfw', q.system.fs.joinPaths(filesexportDir, 'lib', 'python', 'site-packages'))
    recipe.addSource(connection, 'scripts/', q.system.fs.joinPaths(filesexportDir, 'scripts'))
    recipe.addSource(connection, 'docs/', q.system.fs.joinPaths(filesexportDir, 'docs'))
    tmpdir = q.system.fs.joinPaths(filesexportDir, 'tmp')
    recipe.addSource(connection, 'model/tasklets/', tmpdir)
    osis_service_dir = q.system.fs.joinPaths(filesexportDir, 'apps', 'applicationserver', 'services', 'osis_service', 'tasklets')

    recipe.executeTaskletAction(params["action"])

    q.system.fs.copyDirTree(tmpdir, osis_service_dir)
