
__author__ = 'incubaid'
__tags__ = 'package',
__priority__ = 1

def match(q, i, params, tags):
    return True
    
def main(q, i, params, tags):
    
    qpackage = params['qpackage']
    filesDir = qpackage.getPathFiles()
    q.system.fs.removeDirTree(filesDir)
    q.system.fs.createDir(filesDir)
    q.logger.log('Packaging Osis', 1)
    
    egg_dir = q.system.fs.joinPaths(filesDir, 'generic', 'osis_egg')

    site_packages = q.system.fs.joinPaths('generic', 'lib', 'python', 'site-packages')
    base_site_packages = q.system.fs.joinPaths(qpackage.getPathSourceCode(), site_packages)

    egg_zip_name = qpackage.name + '.egg.zip'
    egg_name = q.system.fs.joinPaths(egg_dir, egg_zip_name)
    eggfolder = q.system.fs.joinPaths(base_site_packages, qpackage.name)
    q.system.fs.createDir(eggfolder)
    q.system.fs.createDir(egg_dir)
    q.qpackagetools.createEggZipFromSandboxDir(eggfolder, egg_name)

    relativePath = q.system.fs.joinPaths('generic', 'lib', 'pylabs', 'extensions', 'osis_connection')
    q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackage.getPathSourceCode(), relativePath), q.system.fs.joinPaths(filesDir, relativePath))

