
__author__ = 'aserver'
__tags__   = 'configure',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    PORT = 80
    PATH = 'static'
    ROOT = q.system.fs.joinPaths(q.dirs.baseDir, 'www')
    
    nginx = q.manage.nginx
    
    nginx.startChanges()
    
    cmdb = nginx.cmdb
    
    if str(PORT) not in cmdb.virtualHosts:
        cmdb.addVirtualHost(str(PORT), port=PORT)
    
    vhost = cmdb.virtualHosts[str(PORT)]
    
    if PATH not in vhost.sites:
        site = vhost.addSite(PATH, '/%s' % PATH)
        site.addOption('root', ROOT)
        site.addOption('rewrite ', '^/%s/(.*) /$1 break' % PATH)
        site.addOption('rewrite  ', '^/%s$ /%s/ permanent' % (PATH, PATH))
    
    nginx.save()
    nginx.applyConfig()
     
   
