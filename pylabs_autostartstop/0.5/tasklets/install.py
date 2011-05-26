__author__   = "aserver"
__tags__     = "install",
__priority__ = 1

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    # Copy the files for this platform from the files/ folder to sandbox
    qpackage = params['qpackage']
    qpackage.copyFiles()

    rcFiles = []
    scriptPath = '/etc/init.d/qbase5'
    rcFiles.append('/etc/rc2.d/S80qbase5')
    if q.platform.isLinux(): rcFiles.extend(['/etc/rc0.d/K10qbase5','/etc/rc6.d/K10qbase5'])
    if q.platform.isSolaris(): rcFiles.append('/etc/rc2.d/K80qbase5')
    qshellPath = q.system.fs.joinPaths(q.dirs.baseDir, 'qshell')

    scriptContents = """#!/bin/bash
#
# pylabs_auto_start_stop init script
#
[ -x %(qshellpath)s ] || exit 1
RETVAL=0

. /lib/lsb/init-functions

ulimit -c unlimited

case "$1" in
   start)
      log_daemon_msg "Starting Qbase Services" "qbase"
      PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"
      %(qshellpath)s -c "q.manage.servers.all.start()" > /dev/console 2>&1
      ;;
   stop)
      log_daemon_msg "Stopping Qbase Services" "qbase"
      %(qshellpath)s -c "q.manage.servers.all.stop()" > /dev/console 2>&1
      ;;
   restart)
      PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"
      %(qshellpath)s -c "q.manage.servers.all.stop()" > /dev/console 2>&1
      %(qshellpath)s -c "q.manage.servers.all.start()" > /dev/console 2>&1
      ;;
   *)
      echo "Usage: $0 {start|stop|restart}"
      RETVAL=1
      ;;
esac

exit $RETVAL """ % {'qshellpath' : qshellPath}


    q.system.fs.writeFile(scriptPath, scriptContents)

    q.system.unix.chmod(q.system.fs.getDirName(scriptPath), 0755, filePattern = q.system.fs.getBaseName(scriptPath))
    for rcFile in rcFiles:
        if q.system.fs.isFile(rcFile): q.system.fs.removeFile(rcFile)
        if not q.system.fs.isLink(rcFile): q.system.fs.symlink(scriptPath, rcFile)

