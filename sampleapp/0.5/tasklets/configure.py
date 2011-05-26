
__author__ = 'aserver'
__tags__   = 'configure',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    appnames = ['sampleapp']

    for appname in appnames:
        order = appnames.index(appname) + 1 * 10
        if not appname in i.config.autostart.list():
            i.config.autostart.add(appname, {'command': 'p.application.start(%s)' %appname, 'order': str(order)})

        if not appname in i.config.autostop.list():
            i.config.autostop.add(appname, {'command': 'p.application.stop(%s)' %appname, 'order': str(order)})

