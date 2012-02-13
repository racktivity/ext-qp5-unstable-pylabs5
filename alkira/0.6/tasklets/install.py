__author__ = 'incubaid'
__tags__   = 'install',

def main(q, i, params, tags):
    def ensureDecentStructure(parentdir):
        pagename = q.system.fs.getBaseName(parentdir) + ".md"
        parentpage = q.system.fs.joinPaths(parentdir, pagename)
        if q.system.fs.exists(parentpage):
            destination = q.system.fs.joinPaths(q.system.fs.getParent(parentdir), pagename)
            q.system.fs.moveFile(parentpage, destination)

        subdirs = q.system.fs.listDirsInDir(parentdir.decode('utf-8'))
        for subdir in subdirs:
            ensureDecentStructure(subdir)

    def changeSpacefileNames(pyappdir):
        spacedirpath = q.system.fs.joinPaths(pyappdir, 'portal', 'spaces')
        spacefilespath = q.system.fs.joinPaths(spacedirpath, 'Admin', 'Home', 'Spaces')
        if not q.system.fs.exists(spacedirpath):
            return
        spacedirlist = q.system.fs.listDirsInDir(spacedirpath)
        for fullDirname in spacedirlist:
            dirname = q.system.fs.getBaseName(fullDirname)
            if dirname == 'Admin' or dirname == 'IDE':
                continue
            filepath = q.system.fs.joinPaths(spacefilespath, dirname + '.md')
            if q.system.fs.exists(filepath):
                q.system.fs.renameFile(filepath, q.system.fs.joinPaths(spacefilespath,'s_' + dirname + '.md'))

    pyapps = q.system.fs.listDirsInDir(q.dirs.pyAppsDir)
    for pyapp in pyapps:
        changeSpacefileNames(pyapp)
        spacedir = q.system.fs.joinPaths(pyapp, "portal", "spaces")
        if not q.system.fs.exists(spacedir):
            continue
        spaces = q.system.fs.listDirsInDir(spacedir)
        for space in spaces:
            ensureDecentStructure(space)

    qpackage = params['qpackage']
    qpackage.copyFiles()

