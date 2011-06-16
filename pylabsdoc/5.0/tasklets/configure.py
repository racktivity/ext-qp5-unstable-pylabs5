
__author__ = 'incubaid'
__tags__   = 'configure',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    url = 'http://127.0.0.1/pylabsdoc/'
    q.manage.nginx.startChanges()
    vhost = q.manage.nginx.cmdb.virtualHosts['80']
    rproxy = '/'
    if vhost:
        if rproxy in vhost.reverseproxies:
            q.logger.log('Reverse proxy already defined', level=3)
        else:
            q.logger.log('Add reverse proxy to nginx', level=3)
            vhost.addReverseProxy('/', url, '/')
            q.manage.nginx.save()
            q.manage.nginx.applyConfig()
    else:
        q.logger.log('No virtual host 80 exists!', level=3)
