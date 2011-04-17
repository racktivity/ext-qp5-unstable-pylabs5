
__author__ = 'incubaid'
__tags__ = 'package',
__priority__ = 1

def match(q, i, params, tags):
    return True
    
def main(q, i, params, tags):
    
    qpackage = params['qpackage']
    
    q.logger.log('Packaging Osis', 1)
    
    generic_upload_dir = q.system.fs.joinPaths(qpackage.getPathFiles(),'generic')

    egg_dir = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic', 'osis_egg')

    site_packages = q.system.fs.joinPaths('lib', 'python', 'site-packages')
    base_site_packages = q.system.fs.joinPaths(q.dirs.baseDir, 'var', 'src', site_packages)
    
    for dir in (generic_upload_dir, egg_dir):
	if q.system.fs.exists(dir):q.system.fs.removeDirTree(dir)
        q.system.fs.createDir(dir)

    egg_zip_name = qpackage.name + '.egg.zip'
    egg_name = q.system.fs.joinPaths(egg_dir, egg_zip_name)
    q.qpackagetools.createEggZipFromSandboxDir(q.system.fs.joinPaths(base_site_packages, qpackage.name), egg_name)

    relativePath = q.system.fs.joinPaths('lib', 'pylabs', 'extensions', 'osis_connection')
    q.system.fs.copyDirTree(q.system.fs.joinPaths(q.dirs.varDir, 'src', relativePath), q.system.fs.joinPaths(generic_upload_dir, relativePath))

