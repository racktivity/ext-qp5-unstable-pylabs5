__author__ = 'incubaid'
__tags__   = 'install',

def main(q, i, params, tags):
    def ensureDecentStructure(parentdir):
        pagename = q.system.fs.getBaseName(parentdir) + ".md"
        parentpage = q.system.fs.joinPaths(parentdir, pagename)
        if q.system.fs.exists(parentpage):
            destination = q.system.fs.joinPaths(q.system.fs.getParent(parentdir), pagename)
            q.system.fs.moveFile(parentpage, destination)

        subdirs = q.system.fs.listDirsInDir(parentdir)
        for subdir in subdirs:
            ensureDecentStructure(subdir)


    pyapps = q.system.fs.listDirsInDir(q.dirs.pyAppsDir)
    for pyapp in pyapps:
        spaces = q.system.fs.listDirsInDir(q.system.fs.joinPaths(pyapp, "portal", "spaces"))
        for space in spaces:
            ensureDecentStructure(space)

    qpackage = params['qpackage']
    qpackage.copyFiles()
