__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesDir = q.system.fs.joinPaths(qpackage.getPathFiles())
    q.system.fs.removeDirTree(filesDir)
    q.system.fs.createDir(filesDir)
    # library
    relativePath = q.system.fs.joinPaths('lib', 'python', 'site-packages', 'workflowengine')
    q.system.fs.copyDirTree(q.system.fs.joinPaths(q.dirs.varDir, "src", relativePath), q.system.fs.joinPaths(filesDir, "linux", relativePath))
    # manage extension
    relativePath =  q.system.fs.joinPaths('lib', 'pylabs', 'extensions', 'workflowengine', 'manage')
    q.system.fs.copyDirTree(q.system.fs.joinPaths(q.dirs.varDir, "src", relativePath), q.system.fs.joinPaths(filesDir, "linux", relativePath))
    # Disable extension in package (enabled during configure to prevent configure)
    ext = q.system.fs.joinPaths(filesDir, "linux", relativePath, 'extension.cfg')
    from pylabs import inifile
    ini = inifile.IniFile(ext)
    for section in ini.getSections():
        ini.setParam(section, 'enabled', 0)

    # application
    relativePath =q.system.fs.joinPaths('apps', 'workflowengine', 'bin')
    q.system.fs.copyDirTree(q.system.fs.joinPaths(q.dirs.varDir, 'src', 'apps', 'workflowengine', 'bin'), q.system.fs.joinPaths(filesDir, 'linux', relativePath))

    relativePath =q.system.fs.joinPaths('apps', 'applicationserver', 'services', 'wfe_debug')
    q.system.fs.copyDirTree(q.system.fs.joinPaths(q.dirs.varDir, 'src', relativePath), q.system.fs.joinPaths(filesDir, 'linux', relativePath))
