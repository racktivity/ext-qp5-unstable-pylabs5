__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesDir = qpackage.getPathFiles()
    q.system.fs.removeDirTree(filesDir)
    q.system.fs.createDir(filesDir)
    q.system.fs.copyDirTree(qpackage.getPathSourceCode(), qpackage.getPathFiles())
    # Disable extension in package (enabled during configure to prevent configure)
    relativepath = 'lib/pylabs/extensions/workflowengine/manage'
    ext = q.system.fs.joinPaths(filesDir, "linux", relativepath, 'extension.cfg')
    from pylabs import inifile
    ini = inifile.IniFile(ext)
    for section in ini.getSections():
        ini.setParam(section, 'enabled', 0)

