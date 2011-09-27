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

    def changeSpacefileNames(pyappdir):
        spacedirpath = q.system.fs.joinPaths(pyappdir, 'portal', 'spaces')
        spacefilespath = q.system.fs.joinPaths(spacedirpath, 'Admin', 'Home', 'Spaces')
        spacedirlist = q.system.fs.listDirsInDir(spacedirpath)
        for fullDirname in spacedirlist:
            dirname = q.system.fs.getBaseName(fullDirname)
            if dirname == 'Admin' or dirname == 'IDE':
                continue
            filepath = q.system.fs.joinPaths(spacefilespath, dirname + '.md')
            if q.system.fs.exists(filepath):
                q.system.fs.renameFile(filepath, q.system.fs.joinPaths(spacefilespath,'s_' + dirname + '.md'))

    # pyapps = q.system.fs.listDirsInDir(q.dirs.pyAppsDir)
    pyapps = list()
    for pyapp in pyapps:
        changeSpacefileNames(pyapp)
        spaces = q.system.fs.listDirsInDir(q.system.fs.joinPaths(pyapp, "portal", "spaces"))
        for space in spaces:
            ensureDecentStructure(space)

    qpackage = params['qpackage']
    qpackage.copyFiles()

