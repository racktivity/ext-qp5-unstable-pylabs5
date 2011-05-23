import os
import subprocess
import sys

author__ = 'incubaid'
__tags__ = 'compile',

def main(q, i, params, tags):
    qpackage = params["qpackage"]
    filesexportDir = q.system.fs.joinPaths(qpackage.getPathSourceCode(), str(q.enumerators.PlatformType.GENERIC))
    compilePath = q.system.fs.joinPaths(filesexportDir, 'www', 'jswizards', 'js')
    q.system.process.run('coffee -c jswizards.coffee', cwd=compilePath)

