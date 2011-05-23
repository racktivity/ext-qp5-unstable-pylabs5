__author__ = 'incubaid'
__tags__   = 'codemanagement',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    
    filesexportDir =  q.system.fs.joinPaths(qpackage.getPathSourceCode(), 'generic')

    if q.system.fs.exists(filesexportDir):
        q.system.fs.removeDirTree(filesexportDir)
    
    qpackage.checkoutRecipe()
    q.system.fs.removeDirTree(q.system.fs.joinPaths(filesexportDir, 'cfg', 'qpackages4')) 