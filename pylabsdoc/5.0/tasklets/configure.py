
__author__ = 'incubaid'
__tags__   = 'configure',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    url = 'http://127.0.0.1/pylabsdoc/'
    q.manage.nginx.startChanges()
    vhost = q.manage.nginx.cmdb.virtualHosts['80']
    if vhost:
        vhost.addReverseProxy('/', url, '/')
        q.manage.nginx.save()
        q.mange.nginx.applyConfig()
    else:
        q.logger.log('No virtual host 80 exists!', level=3)
