__author__ = 'incubaid'
__tags__   = 'configure',

def main(q, i, params, tags):
    from osis.store.OsisDB import OsisDB
    import imp
    qpackage = params['qpackage']
    osisDb = OsisDB()

    connectionName = 'main'
    database = 'portal'
    ipaddress = '127.0.0.1'
    login = q.manage.postgresql8.cmdb.rootLogin
    passwd = q.manage.postgresql8.cmdb.rootPasswd
    #create db
    if not database in q.manage.postgresql8.cmdb.databases:
        q.manage.postgresql8.startChanges()
        q.manage.postgresql8.cmdb.addDatabase(database, login)
        q.manage.postgresql8.save()
        q.manage.postgresql8.applyConfig()
    #add connection
    if not connectionName in osisDb.listConnections():
        osisDb.addConnection(connectionName, ipaddress, database, login, passwd)

    connection = osisDb.getConnection(connectionName)

    rootObjectDir = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic', 'libexec','osis' )
    rootObjectFiles = q.system.fs.listFilesInDir(rootObjectDir)

    for fil in rootObjectFiles:
        baseName = fil[len(rootObjectDir)+1:]
        if baseName == "__init__.py" :
            continue
        typeName = baseName[:-3]
        if not connection.schemeExists(typeName):
            connection.createObjectTypeByName(typeName)

    for f in q.system.fs.listFilesInDir(q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic', 'views'), True, "*.py"):
        exitcode, stdout, stderr = q.system.process.runScript(f, stopOnError=False)
        if exitcode != 0:
            raise RuntimeError("Failed to configure view %s with output:\n%s %s" % (f, stdout, stderr))

    #Configure xmlrpc and rest reverse proxies on apache
    changesstarted = False
    appserverCfg = q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'applicationserver.cfg')
    if not q.system.fs.exists(appserverCfg):
        raise RuntimeError('Application server is not installed or not configured !!')
    cfg = q.tools.inifile.open(appserverCfg)

    #xmlrpc
    xmlrpc_port = cfg.getValue('main', 'xmlrpc_port')
    xmlrpc_ip = cfg.getValue('main', 'xmlrpc_ip')
    #rest
    rest_port = cfg.getValue('main', 'rest_port')
    rest_ip = cfg.getValue('main', 'rest_ip')

    if '80' not in q.manage.apache.cmdb.virtualHosts:
        q.manage.apache.startChanges()
        changesstarted = True
        vhost = q.manage.apache.cmdb.addVirtualHost('80', port=80)
    else:
        vhost = q.manage.apache.cmdb.virtualHosts['80']

    if 'rest' not in vhost.reverseproxies:
        if not changesstarted:
            q.manage.apache.startChanges()
            changesstarted = True
            vhost = q.manage.apache.cmdb.virtualHosts['80']
        #Add rest reverse proxy
        vhost.addReverseProxy('rest', 'http://%s:%s/' % (rest_ip, rest_port), '/appserver/rest/')
    if 'xmlrpc' not in vhost.reverseproxies:
        if not changesstarted:
            q.manage.apache.startChanges()
            changesstarted = True
            vhost = q.manage.apache.cmdb.virtualHosts['80']
        #Add xmlrpc reverse proxy
        vhost.addReverseProxy('xmlrpc', 'http://%s:%s/' % (xmlrpc_ip, xmlrpc_port), '/appserver/xmlrpc/')
    if changesstarted:
        q.manage.apache.cmdb.save()
        q.manage.apache.applyConfig()

    syncscript_path = q.system.fs.joinPaths(qpackage.getPathFiles(), 'generic', 'scripts')
    for f in q.system.fs.listFilesInDir(syncscript_path):
        error, stdout, sterr = q.system.process.runScript(f, stopOnError=False)
        if error != 0:
            raise RuntimeError("Failed to run script %s with output:\n%s %s" % (f, stdout, stderr))

    #configure lfw and widget services on applicationserver
    for servicename, classspec in {'lfw': 'lfw.lfw.LFWService', 'widget_service': 'widget_service.WidgetService.WidgetService'}.iteritems():
        if not servicename in i.servers.applicationserver.services.list():
            i.servers.applicationserver.services.add(servicename, {'classspec': classspec})

    if q.manage.applicationserver.isRunning():
        q.manage.applicationserver.restart()
