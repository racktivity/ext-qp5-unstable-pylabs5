
__author__ = 'aserver'
__tags__   = 'configure',

def main(q, i, p, params, tags):
    qpackage = params['qpackage']
    appnames = ['sampleapp']

    # Install sampleapp
    p.application.install(appnames[0])

    for appname in appnames:
        order = appnames.index(appname) + 1 * 10
        if not appname in i.config.autostart.list():
            i.config.autostart.add(appname, {'command': 'p.application.start(%s)' %appname, 'order': str(order)})

        if not appname in i.config.autostop.list():
            i.config.autostop.add(appname, {'command': 'p.application.stop(%s)' %appname, 'order': str(order)})

