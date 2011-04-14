__author__ = 'incubaid'
__tags__ = 'package',

def main(q, i, params, tags):
    package = params["qpackage"]
    
    # Clean old files    
    q.system.fs.removeDirTree(package.getPathFiles())
    
    # Copy source to files 
    q.system.fs.copyDirTree(package.getPathSourceCode(), package.getPathFiles())
    

    
