__author__ = 'incubaid'
__tags__= 'configure',


def main(q, i, params, tags):
    #if not 'main' in i.config.agent.list():
    #    i.config.agent.add('main')
    #elif not all([config in i.config.agent.getConfig('main') for config in ('cron_interval', 'enable_cron')]):
    #    i.config.agent.review('main')
 
    if q.manage.applicationserver.isRunning(): q.manage.applicationserver.stop()
    serviceName = 'agent_service'
    classspec = 'agent_service.WFLAgent.WFLAgent'
    if not serviceName in i.servers.applicationserver.services.list():
        i.servers.applicationserver.services.add(serviceName, {'classspec':classspec})

    q.manage.applicationserver.restart()
